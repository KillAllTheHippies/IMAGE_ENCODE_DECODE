import sqlite3
from datetime import datetime
import json
from PIL import Image
import io
import os

class MessageLogger:
    def __init__(self, db_path='messages.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()
        
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                prompt TEXT NOT NULL,
                image_path TEXT UNIQUE NOT NULL,
                encoding_types TEXT,
                image_size TEXT,
                resolution TEXT,
                thumbnail BLOB,
                parameters TEXT
            )
        ''')
        self.conn.commit()

    def log_message(self, prompt, image_path, encoding_types, 
                   image_size, resolution, parameters):
        try:
            # Create thumbnail
            with Image.open(image_path) as img:
                img.thumbnail((256, 256))
                thumbnail_bytes = io.BytesIO()
                img.save(thumbnail_bytes, format='PNG')
                
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO messages 
                (prompt, image_path, encoding_types, image_size, 
                 resolution, thumbnail, parameters)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                prompt,
                image_path,
                ','.join(encoding_types),
                f"{image_size[0]}x{image_size[1]}", 
                f"{resolution[0]}x{resolution[1]}",
                thumbnail_bytes.getvalue(),
                json.dumps(parameters)
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error logging message: {e}")
            return False

    def get_history(self, limit=100, offset=0):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, timestamp, prompt, image_path, encoding_types,
                   image_size, resolution, parameters 
            FROM messages 
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        return cursor.fetchall()

    def get_thumbnail(self, message_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT thumbnail FROM messages WHERE id = ?
        ''', (message_id,))
        result = cursor.fetchone()
        if result:
            return io.BytesIO(result[0])
        return None

    def cleanup_old_records(self, retention_days):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM messages 
            WHERE timestamp < datetime('now', ?)
        ''', (f'-{retention_days} days',))
        self.conn.commit()
        return cursor.rowcount

    def close(self):
        self.conn.close()