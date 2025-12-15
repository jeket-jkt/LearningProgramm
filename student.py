from database import connect

def register_student(full_name, email, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (full_name, email, password) VALUES (?, ?, ?)",
                (full_name, email, password))
    conn.commit()
    conn.close()

def get_students():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, email FROM students")
    data = cur.fetchall()
    conn.close()
    return data

def check_login(email, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name FROM students WHERE email=? AND password=?", (email, password))
    row = cur.fetchone()
    conn.close()
    return row