import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join('history', 'conversion_log.json')

class ConversionHistory:
    def __init__(self):
        if not os.path.exists('history'):
            os.makedirs('history')
        if not os.path.exists(HISTORY_FILE):
            self._write_history([])

    def _write_history(self, history):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    def get_history(self):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return []

    def add_entry(self, source_files, output, status):
        history = self.get_history()
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": source_files,
            "output": output,
            "status": status
        }
        history.insert(0, entry)
        self._write_history(history)

    def clear_history(self):
        self._write_history([])
