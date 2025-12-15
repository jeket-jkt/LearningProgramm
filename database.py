import sqlite3
from datetime import datetime

DB_NAME = "univer.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE,
        password TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER,
        question_text TEXT,
        correct_answer TEXT,
        FOREIGN KEY(topic_id) REFERENCES topics(id)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        question_id INTEGER,
        student_answer TEXT,
        is_correct INTEGER,
        timestamp TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(question_id) REFERENCES questions(id)
    )
    """)
    conn.commit()
    conn.close()

def insert_answer(student_id, question_id, student_answer, is_correct):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO student_answers
    (student_id, question_id, student_answer, is_correct, timestamp)
    VALUES (?, ?, ?, ?, ?)""",
    (student_id, question_id, student_answer, is_correct, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def delete_question(question_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()