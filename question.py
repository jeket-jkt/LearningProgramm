from database import connect

def get_topics():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM topics ORDER BY id")
    data = cur.fetchall()
    conn.close()
    return data


def get_questions_by_topic(topic_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, question_text, correct_answer FROM questions WHERE topic_id=?", (topic_id,))
    data = cur.fetchall()
    conn.close()
    return data


def add_topic(name, description=""):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO topics (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()


def add_question(topic_id, question_text, correct_answer):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO questions (topic_id, question_text, correct_answer) VALUES (?, ?, ?)",
        (topic_id, question_text, correct_answer)
    )
    conn.commit()
    conn.close()