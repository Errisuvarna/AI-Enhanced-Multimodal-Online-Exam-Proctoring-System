import sqlite3
import os

# 📁 Database file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "exam_system.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ---------------- Users Table ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT CHECK(role IN ('admin', 'student'))
)
""")

# ---------------- Subjects Table ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

# ✅ Insert default subjects
cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES ('Aptitude')")
cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES ('English')")
cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES ('Maths')")
cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES ('Programming')")
print("Default subjects inserted")

# ---------------- Questions Table ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_answer INTEGER,
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
)
""")

# ---------------- Sample Questions ----------------
# Check if questions exist
existing_q = cursor.execute("SELECT COUNT(*) as cnt FROM questions").fetchone()[0]
if existing_q == 0:
    # Get subject IDs
    subjects = cursor.execute("SELECT id, name FROM subjects").fetchall()
    for sub in subjects:
        sub_id = sub[0]
        name = sub[1]
        cursor.execute("""
            INSERT INTO questions (subject_id, question, option1, option2, option3, option4, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sub_id,
              f"This is a sample {name} question?",
              "Option 1", "Option 2", "Option 3", "Option 4",
              1))
    print("Sample questions inserted for all subjects")

# ---------------- Exam Results Table ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS exam_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    subject_id INTEGER,
    score INTEGER,
    total INTEGER,
    time_taken TEXT,
    date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
)
""")

# ---------------- Exam Answers Table ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS exam_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_result_id INTEGER,
    question_id INTEGER,
    selected_option INTEGER,
    correct_option INTEGER,
    is_correct INTEGER,
    FOREIGN KEY(exam_result_id) REFERENCES exam_results(id),
    FOREIGN KEY(question_id) REFERENCES questions(id)
)
""")

# ---------------- FINAL RESULTS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    score INTEGER,
    total INTEGER,
    percentage REAL,
    certificate_type TEXT,
    created_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()
print("Database setup completed successfully!")
