import google.generativeai as genai
from src.config import settings
import time
from typing import Optional

class LLMClient:
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or settings.GOOGLE_API_KEY
        self.model_name = model or settings.MODEL_VERSION
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        self.last_request_time = 0
        self.min_interval = 60 / settings.MAX_REQUESTS_PER_MINUTE
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
    
    def generate_sql(self, question: str, schema: dict, prompt_version: str = "v1") -> Optional[str]:
        self._rate_limit()
        
        schema_str = self._format_schema(schema)
        prompt = self._build_prompt(question, schema_str, prompt_version)
        
        try:
            response = self.model.generate_content(prompt)
            sql = self._extract_sql(response.text)
            return sql
        except Exception as e:
            print(f"LLM Error: {e}")
            return None
    
    def _format_schema(self, schema: dict) -> str:
        lines = []
        for table, columns in schema.items():
            lines.append(f"Table: {table}")
            lines.append(f"Columns: {', '.join(columns)}")
            lines.append("")
        return "\n".join(lines)
    
    def _build_prompt(self, question: str, schema: str, version: str) -> str:
        system_prompt = f\"\"\"You are a SQL expert. Generate SQLite queries for the given schema.

Database Schema:
{schema}

Rules:
- Use SQLite syntax
- Return only the SQL query, no explanation
- Use proper JOINs when needed
- Use aggregate functions appropriately
- Format the query for readability

Question: {question}

SQL Query:\"\"\"
        return system_prompt
    
    def _extract_sql(self, response: str) -> str:
        response = response.strip()
        
        if "```sql" in response:
            start = response.find("```sql") + 6
            end = response.find("```", start)
            return response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            return response[start:end].strip()
        
        return response
