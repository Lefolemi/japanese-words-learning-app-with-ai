import pandas as pd
from database.db_handler import init_db, get_db_connection

def migrate():
    print("Creating database...")
    init_db()
    
    print("Reading CSV...")
    df = pd.read_csv('database/jlpt_vocab.csv')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print(f"Migrating {len(df)} words...")
    for _, row in df.iterrows():
        # Strip 'N' from 'N5' if it exists to store as integer
        level = str(row['JLPT Level']).replace('N', '').replace('JLPT', '').strip()
        
        cursor.execute('''
            INSERT INTO words (original, furigana, english, jlpt_level)
            VALUES (?, ?, ?, ?)
        ''', (row['Original'], row['Furigana'], row['English'], int(level)))
    
    conn.commit()
    conn.close()
    print("Migration Complete! You can now use the Database.")

if __name__ == "__main__":
    migrate()