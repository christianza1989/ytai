#!/usr/bin/env python3
import sqlite3

def check_schema():
    try:
        with sqlite3.connect("data/youtube_channels.db") as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(youtube_channels)")
            columns = cursor.fetchall()
            
            print("YouTube Channels Table Schema:")
            print("=" * 50)
            for col in columns:
                print(f"{col[1]} ({col[2]}) - {col[3]}")
                
            # Also check if table exists and has data
            cursor.execute("SELECT COUNT(*) FROM youtube_channels")
            count = cursor.fetchone()[0]
            print(f"\nTotal records: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM youtube_channels LIMIT 1")
                sample = cursor.fetchone()
                print(f"Sample record: {sample}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_schema()