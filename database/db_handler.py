import sqlite3
import os

DB_PATH = 'database/jp_game.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_db():
    """Creates the table if it doesn't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original TEXT,
            furigana TEXT,
            english TEXT,
            jlpt_level INTEGER,
            is_marked INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def toggle_mark_status(word_id, status):
    """Saves the 'Marked' status to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    # status should be 1 (marked) or 0 (unmarked)
    cursor.execute('UPDATE words SET is_marked = ? WHERE id = ?', (status, word_id))
    conn.commit()
    conn.close()

def get_words_by_deck(level_num, deck_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    limit = 20
    offset = deck_id * 20
    
    # level_num is now 5, 4, 3, etc.
    cursor.execute('SELECT * FROM words WHERE jlpt_level = ? LIMIT ? OFFSET ?', 
                   (level_num, limit, offset))
    
    words = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return words