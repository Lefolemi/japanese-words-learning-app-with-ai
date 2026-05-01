import pandas as pd
import math

CSV_PATH = 'database/jlpt_vocab.csv'

def load_full_dataset():
    return pd.read_csv(CSV_PATH)

def get_decks_for_level(level):
    """Calculates how many 20-word decks exist for a JLPT level"""
    df = load_full_dataset()
    level_df = df[df['JLPT Level'].astype(str).str.contains(level[-1])] # Gets '5' from 'JLPT 5'
    
    total_words = len(level_df)
    num_decks = math.ceil(total_words / 20)
    
    decks = []
    for i in range(num_decks):
        start_idx = i * 20 + 1
        end_idx = min((i + 1) * 20, total_words)
        decks.append({
            'id': i,
            'name': f"Deck {i+1}",
            'range': f"{start_idx} - {end_idx}"
        })
    return decks

def get_words_for_deck(level, deck_id):
    """Grabs the specific 20 words for a session"""
    df = load_full_dataset()
    level_df = df[df['JLPT Level'].astype(str).str.contains(level[-1])]
    
    start = deck_id * 20
    end = start + 20
    return level_df.iloc[start:end].to_dict('records')