import json
from datetime import datetime

def load_json(filepath):
    """Safe JSON file loader with error handling"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {str(e)}")
        return None

def save_conversation(log, user_id="default"):
    """Save conversation to a log file"""
    filename = f"{LOGS_DIR}/conversation_{user_id}_{datetime.now().strftime('%Y%m%d')}.log"
    with open(filename, 'a') as f:
        f.write(f"{datetime.now()} - {log}\n")