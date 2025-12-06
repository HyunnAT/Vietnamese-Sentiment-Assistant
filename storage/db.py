import sqlite3
from datetime import datetime


class Database:
    def __init__(self, path="sentiments.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create()

    # Tạo bảng nếu chưa tồn tại
    def _create(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sentiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                sentiment TEXT,
                score REAL,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    # Chèn bản ghi mới
    def insert_sentiment(self, text, sentiment, score):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(
            "INSERT INTO sentiments (text, sentiment, score, timestamp) VALUES (?, ?, ?, ?)",
            (text, sentiment, score, ts)
        )
        self.conn.commit()

    # Lấy lịch sử phân tích
    def get_history(self, limit=20):
        cur = self.conn.execute(
            "SELECT text, sentiment, score, timestamp FROM sentiments ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return [dict(row) for row in cur.fetchall()]
