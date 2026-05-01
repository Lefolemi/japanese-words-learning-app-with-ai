import sqlite3
import os

DB_PATH = os.path.join('database', 'jp_game.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Check total count
cursor.execute('SELECT COUNT(*) FROM words')
count = cursor.fetchone()[0]
print(f"Total words in DB: {count}")

# 2. Check a sample row
cursor.execute('SELECT * FROM words LIMIT 1')
row = cursor.fetchone()
print(f"Sample data: {row}")

# 3. Check what levels exist
cursor.execute('SELECT DISTINCT jlpt_level FROM words')
levels = cursor.fetchall()
print(f"Levels found in DB: {levels}")

conn.close()