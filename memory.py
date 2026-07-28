import sqlite3
from datetime import datetime


class Memory:
    def __init__(self, database_name="nexus_memory.db"):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def save_message(self, role, content):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO conversations (role, content)
            VALUES (?, ?)
        """, (role, content))

        self.connection.commit()

    def load_messages(self, limit=None):
        cursor = self.connection.cursor()

        if limit is None:
            cursor.execute("""
                SELECT role, content
                FROM conversations
                ORDER BY id
            """)
            return cursor.fetchall()

        cursor.execute("""
            SELECT role, content
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        rows.reverse()
        return rows

    def save_memory(self, memory):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO memories (memory, created_at)
            VALUES (?, ?)
        """, (memory, datetime.now().isoformat()))

        self.connection.commit()

    def load_memories(self, limit=None):
        cursor = self.connection.cursor()

        if limit is None:
            cursor.execute("""
                SELECT memory
                FROM memories
                ORDER BY id
            """)
            return cursor.fetchall()

        cursor.execute("""
            SELECT memory
            FROM memories
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        rows.reverse()
        return rows

    def search_memories(self, query, limit=5):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT memory
            FROM memories
            WHERE memory LIKE ?
            ORDER BY id DESC
            LIMIT ?
        """, (f"%{query}%", limit))

        rows = cursor.fetchall()
        rows.reverse()
        return rows

    def close(self):
        self.connection.close()