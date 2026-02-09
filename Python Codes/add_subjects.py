import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "exam_system.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
# List of subjects to add
subjects = ["Aptitude", "English", "Maths", "Programming"]

for sub in subjects:
    cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES (?)", (sub,))

conn.commit()
conn.close()
print("Subjects added successfully!")
