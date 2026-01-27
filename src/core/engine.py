import pandas as pd
from typing import Tuple
from src.core.llm import LLMClient
from src.core.db import DatabaseClient
from src.core.logger import ExperimentLogger
from src.core.validation import validate_result
import time

class Text2SQLEngine:
    
    def __init__(self, prompt_version: str = "v1"):
        self.llm = LLMClient()
        self.db = DatabaseClient()
        self.logger = ExperimentLogger()
        self.prompt_version = prompt_version
    
    def ask(self, question: str, validate: bool = True) -> Tuple[pd.DataFrame, dict]:
        start_time = time.time()
        metadata = {
            'user_question': question,
            'prompt_version': self.prompt_version,
            'sql': None,
            'success': False,
            'error': None,
            'rows': 0,
            'execution_time_ms': 0,
            'validation_passed': True
        }
        
        try:
            schema = self.db.get_schema_info()
            sql = self.llm.generate_sql(question, schema, self.prompt_version)
            metadata['sql'] = sql
            
            if not sql:
                raise Exception("Failed to generate SQL")
            
            result = self.db.execute_query(sql)
            
            if isinstance(result, str):
                raise Exception(result)
            
            metadata['rows'] = len(result)
            metadata['success'] = True
            
            if validate:
                is_valid, error_msg = validate_result(result)
                metadata['validation_passed'] = is_valid
                if not is_valid:
                    metadata['error'] = error_msg
            
            metadata['execution_time_ms'] = (time.time() - start_time) * 1000
            
            self.logger.log_experiment({
                **metadata,
                'execution_success': metadata['success']
            })
            
            return result, metadata
            
        except Exception as e:
            metadata['error'] = str(e)
            metadata['execution_time_ms'] = (time.time() - start_time) * 1000
            
            self.logger.log_experiment({
                **metadata,
                'execution_success': False
            })
            
            return pd.DataFrame(), metadata
    
    def get_schema(self) -> dict:
        return self.db.get_schema_info()
    
    def get_performance_stats(self) -> dict:
        return self.logger.get_stats()
