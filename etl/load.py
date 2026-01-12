
import sqlite3
import pandas as pd
import logging
import os

DB_NAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tutorials.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            channel_title TEXT,
            published_at TEXT,
            view_count INTEGER,
            like_count INTEGER,
            comment_count INTEGER,
            duration_minutes REAL,
            engagement_score REAL,
            video_type TEXT,
            search_query TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(df):
    if df.empty:
        return
    
    init_db()
    conn = sqlite3.connect(DB_NAME)
    
    # Idempotency check: Get existing IDs
    try:
        existing_ids = pd.read_sql("SELECT video_id FROM videos", conn)['video_id'].tolist()
    except:
        existing_ids = []
    
    # Filter new rows
    new_rows = df[~df['video_id'].isin(existing_ids)]
    
    if not new_rows.empty:
        new_rows.to_sql('videos', conn, if_exists='append', index=False)
        logging.info(f"Added {len(new_rows)} new videos to database.")
    else:
        logging.info("No new videos to add.")
        
    conn.close()

def load_data(query=None):
    init_db()
    conn = sqlite3.connect(DB_NAME)
    if query:
        df = pd.read_sql("SELECT * FROM videos WHERE search_query = ?", conn, params=(query,))
    else:
        df = pd.read_sql("SELECT * FROM videos", conn)
    conn.close()
    return df
