import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "exam_system.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Aptitude Questions
cursor.execute("""
INSERT OR IGNORE INTO questions (subject_id, question, option1, option2, option3, option4, correct_answer)
VALUES ((SELECT id FROM subjects WHERE name='Aptitude'), 'What is 5 + 7?', '10', '11', '12', '13', 3)
""")

# English Questions
cursor.execute("""
INSERT OR IGNORE INTO questions (subject_id, question, option1, option2, option3, option4, correct_answer)
VALUES ((SELECT id FROM subjects WHERE name='English'), 'Select the correct spelling', 'Recieve', 'Receive', 'Recive', 'Receve', 2)
""")

# Maths Questions
cursor.execute("""
INSERT OR IGNORE INTO questions (subject_id, question, option1, option2, option3, option4, correct_answer)
VALUES ((SELECT id FROM subjects WHERE name='Maths'), 'Solve: 8 * 7', '54', '56', '58', '64', 2)
""")

# Programming Questions
cursor.execute("""
INSERT OR IGNORE INTO questions (subject_id, question, option1, option2, option3, option4, correct_answer)
VALUES ((SELECT id FROM subjects WHERE name='Programming'), 'Which language is used for web backend?', 'HTML', 'CSS', 'Python', 'Photoshop', 3)
""")

conn.commit()
conn.close()
print("Example questions added successfully!")
