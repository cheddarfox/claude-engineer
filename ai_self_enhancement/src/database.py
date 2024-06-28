import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_file="ai_enhancement.db"):
        self.db_file = db_file
        self.conn = None
        self.create_tables()

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_file)
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        # Create logs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL
        )
        ''')

        # Create performance_data table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL
        )
        ''')

        conn.commit()
        self.close()

    def log(self, level, message):
        conn = self.connect()
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)",
            (timestamp, level, message)
        )
        conn.commit()
        self.close()

    def store_performance_data(self, metric_name, metric_value):
        conn = self.connect()
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO performance_data (timestamp, metric_name, metric_value) VALUES (?, ?, ?)",
            (timestamp, metric_name, metric_value)
        )
        conn.commit()
        self.close()

    def get_logs(self, limit=100):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        logs = cursor.fetchall()
        self.close()
        return logs

    def get_performance_data(self, metric_name, limit=100):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM performance_data WHERE metric_name = ? ORDER BY timestamp DESC LIMIT ?",
            (metric_name, limit)
        )
        data = cursor.fetchall()
        self.close()
        return data

# Initialize the database
db = Database()