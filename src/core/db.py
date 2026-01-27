import sqlite3
import pandas as pd
from typing import Union
from pathlib import Path
from src.config import settings

class DatabaseClient:
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.DB_PATH
        self._validate_database()
    
    def _validate_database(self):
        if not Path(self.db_path).exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
    
    def execute_query(self, sql: str) -> Union[pd.DataFrame, str]:
        dangerous_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE']
        if any(keyword in sql.upper() for keyword in dangerous_keywords):
            return "Error: Modification queries are not allowed"
        
        try:
            conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return df
        except sqlite3.Error as e:
            return f"SQL Error: {e}"
        except Exception as e:
            return f"Execution Error: {e}"
    
    def get_schema_info(self) -> dict:
        schema = {}
        
        try:
            conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                columns = [row[1] for row in cursor.fetchall()]
                schema[table] = columns
            
            conn.close()
            return schema
        except Exception as e:
            print(f"Schema Error: {e}")
            return {}
    
    def get_sample_data(self, table: str, n: int = 5) -> pd.DataFrame:
        sql = f"SELECT * FROM {table} LIMIT {n};"
        return self.execute_query(sql)
