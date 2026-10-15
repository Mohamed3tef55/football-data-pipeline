import csv
import sqlite3
import os

RAW_DATA_PATH = "data/players.csv"
DB_PATH = "data/football.db"

def extract_data(file_path):
    """قراءة البيانات من ملف CSV"""
    print(" [1/3] Extracting data from CSV...")
    records = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
    return records

def transform_data(raw_records):
    """تنظيف البيانات وتجهيزها"""
    print(" [2/3] Transforming and cleaning data...")
    cleaned_records = []
    
    for row in raw_records:
        name = row["name"].strip()
        club = row["club"].strip()
        
        # استبعاد الصف إذا كان اسم اللاعب فارغاً
        if not name:
            continue
            
        # معالجة الأهداف (تحويل لنص ثم لرقم، وإن كانت فارغة نجعلها 0)
        goals_raw = row["goals"].strip()
        goals = int(goals_raw) if goals_raw else 0
        
        # معالجة القيمة السوقية (تحويلها لـ float، وإن كانت فارغة نجعلها 0.0)
        market_val_raw = row["market_value_m"].strip()
        market_value = float(market_val_raw) if market_val_raw else 0.0
        
        cleaned_records.append({
            "player_id": int(row["player_id"]),
            "name": name,
            "club": club,
            "goals": goals,
            "market_value_m": market_value
        })
        
    return cleaned_records

def load_data(records, db_path):
    """تخزين البيانات في قاعدة بيانات SQLite باستخدام SQL"""
    print(" [3/3] Loading cleaned data into SQLite database...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. إنشاء الجدول إذا لم يكن موجوداً
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        club TEXT NOT NULL,
        goals INTEGER DEFAULT 0,
        market_value_m REAL DEFAULT 0.0
    );
    """)
    
    # 2. إدخال أو تحديث البيانات
    for record in records:
        cursor.execute("""
        INSERT OR REPLACE INTO players (player_id, name, club, goals, market_value_m)
        VALUES (?, ?, ?, ?, ?);
        """, (
            record["player_id"],
            record["name"],
            record["club"],
            record["goals"],
            record["market_value_m"]
        ))
        
    conn.commit()
    conn.close()
    print(" Data Pipeline executed successfully!")

def verify_data(db_path):
    """قراءة واستعراض ما تم حفظه للتأكد"""
    print("\n--- Current Data in Database (SQL Query: SELECT * FROM players) ---")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players;")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]:<18} | Club: {row[2]:<12} | Goals: {row[3]:<2} | Value: €{row[4]}M")
        
    conn.close()

if __name__ == "__main__":
    raw_data = extract_data(RAW_DATA_PATH)
    clean_data = transform_data(raw_data)
    load_data(clean_data, DB_PATH)
    verify_data(DB_PATH)