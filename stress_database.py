import sqlite3

class StressDatabase:
    def __init__(self, db_name="stress.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            score INTEGER,
            level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def insert_result(self, name, gender, score, level):
        self.cursor.execute("""
        INSERT INTO results (name, gender, score, level)
        VALUES (?, ?, ?, ?)
        """, (name, gender, score, level))
        self.conn.commit()

    def fetch_all_results(self):
        self.cursor.execute("SELECT * FROM results")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()