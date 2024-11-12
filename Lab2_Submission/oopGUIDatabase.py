import sys
import csv
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QLabel, QMessageBox, QFileDialog,
    QComboBox, QTabWidget, QHBoxLayout, QFormLayout, QDialog, QDialogButtonBox
)

DATABASE = 'university.db'

def execute_query(query, params=(), fetchone=False, fetchall=False):
    """
    Execute a SQL query on the database.

    Args:
        query (str): SQL query to be executed.
        params (tuple, optional): Parameters to bind to the SQL query.
        fetchone (bool, optional): Fetch only the first row of the result.
        fetchall (bool, optional): Fetch all rows of the result.

    Returns:
        tuple or list of tuples: The result of the query, depending on fetchone or fetchall.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()
    else:
        conn.commit()
        result = None
    conn.close()
    return result

def fetch_students():
    """
    Fetch all student records from the database.

    Returns:
        list of tuple: List containing all student records.
    """
    return execute_query('SELECT * FROM students', fetchall=True)

def fetch_instructors():
    """
    Fetch all instructor records from the database.

    Returns:
        list of tuple: List containing all instructor records.
    """
    return execute_query('SELECT * FROM instructors', fetchall=True)

def fetch_courses():
    """
    Fetch all courses along with their assigned instructors from the database.

    Returns:
        list of tuple: List containing course records with instructor details.
    """
    return execute_query('SELECT courses.id, title, code, name FROM courses LEFT JOIN instructors ON courses.instructor_id = instructors.id', fetchall=True)

def insert_student(name, age, email):
    """
    Insert a new student into the database.

    Args:
        name (str): The name of the student.
        age (int): The age of the student.
        email (str): The email address of the student.
    """
    execute_query('INSERT INTO students (name, age, email) VALUES (?, ?, ?)', (name, age, email))

def insert_instructor(name, department):
    """
    Insert a new instructor into the database.

    Args:
        name (str): The name of the instructor.
        department (str): The department of the instructor.
    """
    execute_query('INSERT INTO instructors (name, department) VALUES (?, ?)', (name, department))

def insert_course(title, code, instructor_id):
    """
    Insert a new course into the database.

    Args:
        title (str): The title of the course.
        code (str): The code of the course.
        instructor_id (int): The ID of the instructor assigned to the course.
    """
    execute_query('INSERT INTO courses (title, code, instructor_id) VALUES (?, ?, ?)', (title, code, instructor_id))

def assign_student_to_course(course_id, student_id):
    """
    Assign a student to a specific course.

    Args:
        course_id (int): The ID of the course.
        student_id (int): The ID of the student.
    """
    execute_query('INSERT INTO course_students (course_id, student_id) VALUES (?, ?)', (course_id, student_id))

def assign_instructor_to_course(course_id, instructor_id):
    """
    Assign an instructor to a specific course.

    Args:
        course_id (int): The ID of the course.
        instructor_id (int): The ID of the instructor.
    """
    execute_query('UPDATE courses SET instructor_id = ? WHERE id = ?', (instructor_id, course_id))

class MainWindow(QWidget):
    """
    Main application window for the University Management System.

    This class handles the creation of the GUI, including setting up tabs and widgets for managing
    students, instructors, courses, and assignments.
    """

    def __init__(self):
        """
        Initialize the main window and setup the UI components.
        """
        super().__init__()
        self.setWindowTitle("University Management System")
        self.resize(1000, 600)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_students_tab(), "Students")
        self.tabs.addTab(self.create_instructors_tab(), "Instructors")
        self.tabs.addTab(self.create_courses_tab(), "Courses")
        self.tabs.addTab(self.create_assignments_tab(), "Assignments")
        self.tabs.addTab(self.create_all_records_tab(), "All Records")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_students_tab(self):
        """
        Creates and returns the Students tab for the main window.

        Returns:
            QWidget: The Students tab with layout and widgets configured.
        """
        layout = QVBoxLayout()
        self.students_table = QTableWidget(0, 4)
        self.students_table.setHorizontalHeaderLabels(["Name", "Age", "Email", "Actions"])
        self.refresh_students_table()
        layout.addWidget(self.students_table)

        form_layout = QFormLayout()
        self.student_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_email_input = QLineEdit()
        form_layout.addRow("Name:", self.student_name_input)
        form_layout.addRow("Age:", self.student_age_input)
        form_layout.addRow("Email:", self.student_email_input)
        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        export_button = QPushButton("Export Students to CSV")
        export_button.clicked.connect(self.export_students_to_csv)
        layout.addWidget(export_button)

        container = QWidget()
        container.setLayout(layout)
        return container

    # Similar docstrings for other methods within MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
