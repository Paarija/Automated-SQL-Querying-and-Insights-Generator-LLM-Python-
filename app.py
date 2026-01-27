import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.core.engine import Text2SQLEngine
from src.config import settings, validate_paths
from src.core.validation import check_data_quality

st.set_page_config(
    page_title="Text2SQL Studio",
    page_icon="📊",
    layout="wide"
)

if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

if 'engine' not in st.session_state:
    try:
        validate_paths()
        st.session_state.engine = Text2SQLEngine(prompt_version="v1")
        st.session_state.initialized = True
        st.session_state.api_key_configured = True
    except Exception as e:
        st.session_state.initialized = False
        st.session_state.error = str(e)
        st.session_state.api_key_configured = False

with st.sidebar:
    st.title("🔧 Data Control Panel")
    
    st.subheader("🔑 API Configuration")
    
    api_key_input = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="Enter your API key here...",
        help="Get your free API key at https://aistudio.google.com/app/apikey",
        key="api_key_widget"
    )
    
    col1, col2 = st.columns(2)
    
    if col1.button("💾 Save & Apply", type="primary", use_container_width=True):
        if api_key_input and len(api_key_input) > 10:
            try:
                import os
                os.environ['GOOGLE_API_KEY'] = api_key_input
                
                env_path = Path(".env")
                if env_path.exists():
                    with open(env_path, 'r') as f:
                        lines = f.readlines()
                    
                    with open(env_path, 'w') as f:
                        for line in lines:
                            if line.startswith('GOOGLE_API_KEY='):
                                f.write(f'GOOGLE_API_KEY={api_key_input}\n')
                            else:
                                f.write(line)
                
                if 'engine' in st.session_state:
                    del st.session_state['engine']
                if 'initialized' in st.session_state:
                    del st.session_state['initialized']
                
                st.success("✅ API key saved! Refreshing...")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please enter a valid API key")
    
    if col2.button("ℹ️ Get API Key", use_container_width=True):
        st.info("👉 Visit: https://aistudio.google.com/app/apikey")
    
    st.divider()
    
    if not st.session_state.initialized:
        st.error("❌ Initialization Failed")
        with st.expander("🔍 View Error Details"):
            st.code(st.session_state.error)
        st.warning("👆 Please configure your API key above and click 'Save & Apply'")
        st.stop()
    
    db_path = Path(settings.DB_PATH)
    if db_path.exists():
        st.success("✅ Database Connected")
        st.caption(f"📂 {settings.DB_PATH}")
    else:
        st.error("❌ Database Missing!")
        st.stop()
    
    with st.expander("📂 View Database Schema", expanded=False):
        schema = st.session_state.engine.get_schema()
        for table, columns in schema.items():
            st.markdown(f"**{table.upper()}**")
            st.caption(", ".join(columns))
            st.divider()
    
    with st.expander("📈 Performance Stats"):
        stats = st.session_state.engine.get_performance_stats()
        st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
        
        if stats['recent_experiments']:
            st.caption("Recent Queries:")
            for exp in stats['recent_experiments'][-3:]:
                status = "✓" if exp.get('execution_success') else "✗"
                st.caption(f"{status} {exp.get('user_question', 'N/A')[:30]}...")

st.title("📊 Text2SQL Studio")
st.caption("Convert natural language to SQL queries using AI")

col1, col2, col3 = st.columns(3)

query = ""
if col1.button("💰 Top Profit Products", use_container_width=True):
    query = "List the top 5 products by total profit."
if col2.button("🌍 Revenue by Region", use_container_width=True):
    query = "Show total revenue grouped by region."
if col3.button("🏆 Best Customers", use_container_width=True):
    query = "Who are the top 5 clients by sales volume?"

user_input = st.text_input(
    "💬 Ask a business question:",
    value=query,
    placeholder="e.g., What is the profit margin for each product category?"
)

if user_input:
    with st.spinner("🔍 Analyzing your question..."):
        result, metadata = st.session_state.engine.ask(user_input, validate=True)
        
        with st.expander("🔧 View Generated SQL"):
            if metadata['sql']:
                st.code(metadata['sql'], language="sql")
            else:
                st.error("Failed to generate SQL")
        
        if metadata['success'] and result is not None and not result.empty:
            st.success("✅ Query executed successfully!")
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Rows Returned", metadata['rows'])
            col_b.metric("Execution Time", f"{metadata['execution_time_ms']:.0f}ms")
            col_c.metric("Validation", "✓ Passed" if metadata['validation_passed'] else "✗ Failed")
            
            if not metadata['validation_passed']:
                st.warning(f"⚠️ Validation Warning: {metadata['error']}")
            
            st.subheader("📋 Results")
            st.dataframe(result, use_container_width=True)
            
            with st.expander("🔍 Data Quality Report"):
                quality = check_data_quality(result)
                st.json(quality)
            
            st.subheader("📊 Visualization")
            numeric_cols = result.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) > 0 and len(result) > 1:
                text_cols = result.columns.difference(numeric_cols)
                
                if len(text_cols) > 0:
                    x_col = text_cols[0]
                    y_col = numeric_cols[0]
                    
                    if "region" in x_col.lower() or "category" in x_col.lower():
                        chart = alt.Chart(result).mark_arc(innerRadius=50).encode(
                            theta=alt.Theta(field=y_col, type="quantitative"),
                            color=alt.Color(field=x_col, type="nominal", legend=alt.Legend(title=x_col)),
                            tooltip=[x_col, y_col]
                        ).properties(
                            title=f"{y_col} Distribution by {x_col}",
                            width=400,
                            height=400
                        )
                    else:
                        chart = alt.Chart(result).mark_bar().encode(
                            x=alt.X(x_col, sort=None, axis=alt.Axis(labelAngle=-45, title=x_col)),
                            y=alt.Y(y_col, title=y_col),
                            tooltip=[x_col, y_col],
                            color=alt.Color(x_col, legend=None)
                        ).properties(
                            title=f"{y_col} by {x_col}"
                        ).interactive()
                    
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info("Chart generation skipped: No categorical columns for X-axis")
            else:
                st.info("Chart generation skipped: Insufficient data or no numeric columns")
        
        elif metadata['success'] and (result is None or result.empty):
            st.warning("⚠️ Query executed but returned no data")
        
        else:
            st.error(f"❌ Query failed: {metadata['error']}")

st.divider()
st.caption("💡 Tip: Be specific with your questions. Include time periods, regions, or product categories for better results.")
