from database import connect, insert_answer

def get_all_answers():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.full_name, q.question_text, sa.student_answer, sa.is_correct
        FROM student_answers sa
        JOIN students s ON sa.student_id = s.id
        JOIN questions q ON sa.question_id = q.id
    """)
    data = cur.fetchall()
    conn.close()
    return data