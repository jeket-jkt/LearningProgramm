from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from student import register_student, check_login

class AuthWindow(QWidget):
    def __init__(self, on_auth_success):
        super().__init__()
        self.on_auth_success = on_auth_success
        self.setWindowTitle('Авторизация / Регистрация')
        self.resize(360, 250)
        self.layout = QVBoxLayout()

        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText('ФИО')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.status_label = QLabel()
        self.toggle_button = QPushButton('Переключить режим')
        self.auth_button = QPushButton('Войти')

        self.layout.addWidget(self.fullname_input)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.auth_button)
        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.status_label)
        self.setLayout(self.layout)

        self.mode = 'login'
        self.update_ui()

        self.toggle_button.clicked.connect(self.toggle_mode)
        self.auth_button.clicked.connect(self.process_auth)

    def toggle_mode(self):
        self.mode = 'register' if self.mode == 'login' else 'login'
        self.update_ui()
        self.status_label.setText('')

    def update_ui(self):
        if self.mode == 'login':
            self.auth_button.setText('Войти')
            self.toggle_button.setText('Регистрация')
        else:
            self.auth_button.setText('Зарегистрироваться')
            self.toggle_button.setText('У меня есть аккаунт')

    def process_auth(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        fullname = self.fullname_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните Email и Пароль")
            return

        if self.mode == 'login':
            student = check_login(email, password)
            if student:
                self.on_auth_success(student[0], student[1])
                self.close()
            else:
                self.status_label.setText('Неверный Email или пароль')
        else:
            if not fullname:
                QMessageBox.warning(self, "Ошибка", "Введите ФИО для регистрации")
                return
            try:
                register_student(fullname, email, password)
                self.status_label.setText('Регистрация успешна. Войдите.')
                self.toggle_mode()
            except Exception as e:
                self.status_label.setText('Ошибка регистрации')