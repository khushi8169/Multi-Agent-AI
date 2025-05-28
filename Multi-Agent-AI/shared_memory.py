import sqlite3
from datetime import datetime

DB_NAME = "shared_memory.db"

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            file_type TEXT,
            intent TEXT,
            timestamp TEXT,
            extracted_fields TEXT,
            thread_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_entry(source, file_type, intent, extracted_fields, thread_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO memory (source, file_type, intent, timestamp, extracted_fields, thread_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (source, file_type, intent, datetime.now().isoformat(), str(extracted_fields), thread_id))
    conn.commit()
    conn.close()

def fetch_all_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM memory')
    rows = cursor.fetchall()
    conn.close()
    return rows
