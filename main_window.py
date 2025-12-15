from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from database import connect, insert_answer
from question import get_topics, get_questions_by_topic, add_topic, add_question
from answer import get_all_answers


class MainWindow(QMainWindow):
    def __init__(self, student_id, student_name):
        super().__init__()
        self.student_id = student_id
        self.student_name = student_name
        self.setWindowTitle('Обучающая система')
        self.resize(900, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_learning_tab()
        self.init_results_tab()
        self.init_admin_tab()

    # ------------------- Вкладка Обучение -------------------
    def init_learning_tab(self):
        self.tab_learning = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f'Добро пожаловать, {self.student_name} (ID {self.student_id})'))

        self.topics_box = QComboBox()
        self.topics_box.addItem("Выберите тему", 0)
        for topic in get_topics():
            self.topics_box.addItem(topic[1], topic[0])
        self.topics_box.currentIndexChanged.connect(self.load_questions)
        layout.addWidget(QLabel("Темы"))
        layout.addWidget(self.topics_box)

        self.questions_box = QComboBox()
        self.questions_box.addItem("Выберите вопрос", 0)
        layout.addWidget(QLabel("Вопросы"))
        layout.addWidget(self.questions_box)

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Ваш ответ")
        layout.addWidget(self.answer_input)

        submit_btn = QPushButton("Отправить ответ")
        submit_btn.clicked.connect(self.submit_answer)
        layout.addWidget(submit_btn)

        self.tab_learning.setLayout(layout)
        self.tabs.addTab(self.tab_learning, "Обучение")

    def load_questions(self):
        topic_id = self.topics_box.currentData()
        self.questions_box.clear()
        self.questions_box.addItem("Выберите вопрос", 0)
        if topic_id == 0:
            return
        questions = get_questions_by_topic(topic_id)
        for q in questions:
            self.questions_box.addItem(q[1], q[0])

    def submit_answer(self):
        question_id = self.questions_box.currentData()
        if question_id == 0:
            QMessageBox.warning(self, "Ошибка", "Выберите вопрос")
            return
        student_answer = self.answer_input.text().strip()
        if not student_answer:
            QMessageBox.warning(self, "Ошибка", "Введите ответ")
            return

        conn = connect()
        cur = conn.cursor()
        correct_answer = cur.execute(
            "SELECT correct_answer FROM questions WHERE id=?",
            (question_id,)
        ).fetchone()[0]
        conn.close()

        is_correct = int(student_answer.lower() == correct_answer.lower())
        insert_answer(self.student_id, question_id, student_answer, is_correct)

        QMessageBox.information(self, "Результат", f"Ответ {'верный' if is_correct else 'неверный'}")
        self.answer_input.clear()
        self.load_results()

    # ------------------- Вкладка Результаты -------------------
    def init_results_tab(self):
        self.tab_results = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Ваши ответы и результаты"))

        self.results_table = QTableWidget()
        self.results_table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.results_table)

        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.tab_results.setLayout(layout)
        self.tabs.addTab(self.tab_results, "Результаты")

        self.load_results()

    def load_results(self):
        data = get_all_answers()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Студент", "Вопрос", "Ответ", "Верно?"])
        self.results_table.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, col in enumerate(row):
                self.results_table.setItem(i, j, QTableWidgetItem(str(col)))

        self.results_table.resizeColumnsToContents()
        self.results_table.resizeRowsToContents()

    # ------------------- Вкладка Админ -------------------
    def init_admin_tab(self):
        self.tab_admin = QWidget()
        layout = QVBoxLayout()

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Название темы")
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Текст вопроса")
        self.correct_input = QLineEdit()
        self.correct_input.setPlaceholderText("Правильный ответ")

        add_btn = QPushButton("Добавить вопрос")
        add_btn.clicked.connect(self.add_question_to_db)

        delete_btn = QPushButton("Удалить выбранный вопрос")
        delete_btn.clicked.connect(self.delete_question_from_db)

        layout.addWidget(QLabel("Добавление темы/вопроса"))
        layout.addWidget(self.topic_input)
        layout.addWidget(self.question_input)
        layout.addWidget(self.correct_input)
        layout.addWidget(add_btn)
        layout.addWidget(delete_btn)

        # Таблица со всеми вопросами
        self.questions_table = QTableWidget()
        self.questions_table.setColumnCount(3)
        self.questions_table.setHorizontalHeaderLabels(["ID", "Вопрос", "Ответ"])
        self.questions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.questions_table)

        self.tab_admin.setLayout(layout)
        self.tabs.addTab(self.tab_admin, "Админ")

        self.load_questions_admin()

    def load_questions_admin(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT id, question_text, correct_answer FROM questions ORDER BY id")
        data = cur.fetchall()
        conn.close()

        self.questions_table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                self.questions_table.setItem(i, j, QTableWidgetItem(str(col)))

    def add_question_to_db(self):
        topic_name = self.topic_input.text().strip()
        question_text = self.question_input.text().strip()
        correct_answer = self.correct_input.text().strip()

        if not topic_name or not question_text or not correct_answer:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        try:
            topics = get_topics()
            topic_id = None
            for t in topics:
                if t[1].lower() == topic_name.lower():
                    topic_id = t[0]
                    break
            if topic_id is None:
                add_topic(topic_name)
                topics = get_topics()
                topic_id = [t[0] for t in topics if t[1].lower() == topic_name.lower()][0]

            add_question(topic_id, question_text, correct_answer)
            QMessageBox.information(self, "Успех", "Вопрос добавлен")

            self.topic_input.clear()
            self.question_input.clear()
            self.correct_input.clear()

            self.load_questions_admin()
            self.refresh_learning_tab()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка:\n{e}")

    def delete_question_from_db(self):
        selected = self.questions_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите вопрос для удаления!")
            return

        question_id = int(self.questions_table.item(selected, 0).text())

        confirm = QMessageBox.question(
            self, "Подтверждение",
            f"Вы действительно хотите удалить вопрос ID {question_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            conn = connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM questions WHERE id=?", (question_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Вопрос удалён")
            self.load_questions_admin()
            self.refresh_learning_tab()

    def refresh_learning_tab(self):
        self.topics_box.clear()
        self.topics_box.addItem("Выберите тему", 0)
        for topic in get_topics():
            self.topics_box.addItem(topic[1], topic[0])
        self.questions_box.clear()
        self.questions_box.addItem("Выберите вопрос", 0)