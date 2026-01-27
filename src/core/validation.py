import pandera as pa
from pandera import Column, DataFrameSchema, Check
import pandas as pd
from typing import Tuple

financial_schema = DataFrameSchema({
    "revenue": Column(float, checks=Check.ge(0), nullable=True, coerce=True),
    "profit": Column(float, nullable=True, coerce=True),
}, strict=False)

regional_schema = DataFrameSchema({
    "region": Column(str, checks=Check.isin(["asia pacific", "europe", "latin america", "north america"]), nullable=False),
}, strict=False)

category_schema = DataFrameSchema({
    "category": Column(str, nullable=False),
}, strict=False)

quantity_schema = DataFrameSchema({
    "quantity": Column(int, checks=Check.ge(0), nullable=False, coerce=True),
}, strict=False)

def validate_result(df: pd.DataFrame, schema_type: str = "auto") -> Tuple[bool, str]:
    if df.empty:
        return True, ""
    
    try:
        if schema_type == "auto":
            if any(col in df.columns for col in ["revenue", "profit"]):
                schema_type = "financial"
            elif "region" in df.columns:
                schema_type = "regional"
            elif "category" in df.columns:
                schema_type = "category"
            elif "quantity" in df.columns:
                schema_type = "quantity"
            else:
                return True, ""
        
        if schema_type == "financial":
            financial_schema.validate(df, lazy=True)
        elif schema_type == "regional":
            regional_schema.validate(df, lazy=True)
        elif schema_type == "category":
            category_schema.validate(df, lazy=True)
        elif schema_type == "quantity":
            quantity_schema.validate(df, lazy=True)
        
        return True, ""
    
    except pa.errors.SchemaError as e:
        error_msg = f"Validation Failed: {str(e)}"
        return False, error_msg

def check_data_quality(df: pd.DataFrame) -> dict:
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": df.duplicated().sum(),
        "numeric_columns": list(df.select_dtypes(include=['number']).columns),
        "text_columns": list(df.select_dtypes(include=['object']).columns),
    }
    
    for col in report["numeric_columns"]:
        negative_count = (df[col] < 0).sum()
        if negative_count > 0:
            report[f"{col}_negative_values"] = negative_count
    
    return report
