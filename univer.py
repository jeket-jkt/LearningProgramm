import sys
from PyQt6.QtWidgets import QApplication
from database import init_db
from auth import AuthWindow
from main_window import MainWindow

def open_main_window(student_id, student_name):
    main_window = MainWindow(student_id, student_name)
    main_window.show()
    app.main_window = main_window

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    auth_window = AuthWindow(on_auth_success=open_main_window)
    auth_window.show()
    sys.exit(app.exec())