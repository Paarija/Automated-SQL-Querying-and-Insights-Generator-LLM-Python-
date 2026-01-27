import pandas as pd
from pathlib import Path
from src.config import settings
from typing import Dict, List

class ExperimentLogger:
    
    def __init__(self, log_file: str = None):
        self.log_file = Path(log_file or settings.LOG_FILE)
        self._ensure_log_exists()
    
    def _ensure_log_exists(self):
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.log_file.exists():
            df = pd.DataFrame(columns=[
                'timestamp', 'user_question', 'sql', 'prompt_version',
                'execution_success', 'rows', 'execution_time_ms', 'error'
            ])
            df.to_csv(self.log_file, index=False)
    
    def log_experiment(self, data: dict):
        try:
            df = pd.read_csv(self.log_file)
            
            new_row = pd.DataFrame([{
                'timestamp': pd.Timestamp.now(),
                'user_question': data.get('user_question', ''),
                'sql': data.get('sql', ''),
                'prompt_version': data.get('prompt_version', ''),
                'execution_success': data.get('execution_success', False),
                'rows': data.get('rows', 0),
                'execution_time_ms': data.get('execution_time_ms', 0),
                'error': data.get('error', '')
            }])
            
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.log_file, index=False)
        except Exception as e:
            print(f"Logging Error: {e}")
    
    def get_stats(self) -> Dict:
        try:
            df = pd.read_csv(self.log_file)
            
            total = len(df)
            successes = df['execution_success'].sum()
            
            return {
                'total_queries': total,
                'successful_queries': successes,
                'success_rate': (successes / total * 100) if total > 0 else 0,
                'recent_experiments': df.tail(10).to_dict('records')
            }
        except Exception as e:
            return {
                'total_queries': 0,
                'successful_queries': 0,
                'success_rate': 0,
                'recent_experiments': []
            }
