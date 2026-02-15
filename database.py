import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self, db_name='movie_recommend.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ratings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_title TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, movie_title)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute(
            "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        user = cursor.fetchone()
        conn.close()
        
        return user
    
    def add_rating(self, user_id, movie_title, rating, description):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                '''INSERT OR REPLACE INTO ratings 
                   (user_id, movie_title, rating, description) 
                   VALUES (?, ?, ?, ?)''',
                (user_id, movie_title, rating, description)
            )
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()
    
    def get_user_ratings(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT movie_title, rating, description, created_at FROM ratings WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        
        ratings = cursor.fetchall()
        conn.close()
        
        return ratings
    
    def get_movie_ratings(self, movie_title):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''SELECT rating, description, u.username, r.created_at 
               FROM ratings r 
               JOIN users u ON r.user_id = u.id 
               WHERE r.movie_title = ? 
               ORDER BY r.created_at DESC''',
            (movie_title,)
        )
        
        ratings = cursor.fetchall()
        conn.close()
        
        return ratings
