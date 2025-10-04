import sqlite3
import os

# Make sure the folder exists
os.makedirs("db/photos", exist_ok=True)

db_path = "db/citizen_observations.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS CitizenObservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    location_lat REAL,
    location_lon REAL,
    date_observed TEXT,
    plant_type TEXT,
    intensity TEXT,
    photo_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("SQLite database and table created at", db_path)
