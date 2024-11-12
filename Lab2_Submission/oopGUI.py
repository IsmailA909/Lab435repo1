import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QLabel, QMessageBox, QFileDialog,
    QComboBox, QTabWidget, QHBoxLayout, QFormLayout, QDialog, QDialogButtonBox
)

# Define the data structures
students = []
instructors = []
courses = []

class Student:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

class Instructor:
    def __init__(self, name, department):
        self.name = name
        self.department = department

class Course:
    def __init__(self, title, code):
        self.title = title
        self.code = code
        self.instructor = None
        self.students = []

# CRUD Dialogs
class CRUDDialog(QDialog):
    def __init__(self, title, headers, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setLayout(QVBoxLayout())
        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))
        self.data = data

        for row_index, item in enumerate(data):
            for col_index, value in enumerate(item):
                self.table.setItem(row_index, col_index, QTableWidgetItem(value))
        
        self.layout().addWidget(self.table)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout().addWidget(self.button_box)

    def get_selected_row(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            return row
        return None

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Management System")
        self.resize(1000, 600)

        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_students_tab(), "Students")
        self.tabs.addTab(self.create_instructors_tab(), "Instructors")
        self.tabs.addTab(self.create_courses_tab(), "Courses")
        self.tabs.addTab(self.create_assignments_tab(), "Assignments")
        self.tabs.addTab(self.create_all_records_tab(), "All Records")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_students_tab(self):
        layout = QVBoxLayout()
        self.students_table = QTableWidget(0, 4)
        self.students_table.setHorizontalHeaderLabels(["Name", "Age", "Email", "Actions"])
        self.refresh_students_table()
        layout.addWidget(self.students_table)

        # Add student form
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

        # Export to CSV button
        export_button = QPushButton("Export Students to CSV")
        export_button.clicked.connect(self.export_students_to_csv)
        layout.addWidget(export_button)

        container = QWidget()
        container.setLayout(layout)
        return container

    def create_instructors_tab(self):
        layout = QVBoxLayout()
        self.instructors_table = QTableWidget(0, 3)
        self.instructors_table.setHorizontalHeaderLabels(["Name", "Department", "Actions"])
        self.refresh_instructors_table()
        layout.addWidget(self.instructors_table)

        # Add instructor form
        form_layout = QFormLayout()
        self.instructor_name_input = QLineEdit()
        self.instructor_department_input = QLineEdit()
        form_layout.addRow("Name:", self.instructor_name_input)
        form_layout.addRow("Department:", self.instructor_department_input)
        add_button = QPushButton("Add Instructor")
        add_button.clicked.connect(self.add_instructor)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        # Export to CSV button
        export_button = QPushButton("Export Instructors to CSV")
        export_button.clicked.connect(self.export_instructors_to_csv)
        layout.addWidget(export_button)

        container = QWidget()
        container.setLayout(layout)
        return container

    def create_courses_tab(self):
        layout = QVBoxLayout()
        self.courses_table = QTableWidget(0, 4)
        self.courses_table.setHorizontalHeaderLabels(["Title", "Code", "Instructor", "Actions"])
        self.refresh_courses_table()
        layout.addWidget(self.courses_table)

        # Add course form
        form_layout = QFormLayout()
        self.course_title_input = QLineEdit()
        self.course_code_input = QLineEdit()
        form_layout.addRow("Title:", self.course_title_input)
        form_layout.addRow("Code:", self.course_code_input)
        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_course)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        # Export to CSV button
        export_button = QPushButton("Export Courses to CSV")
        export_button.clicked.connect(self.export_courses_to_csv)
        layout.addWidget(export_button)

        container = QWidget()
        container.setLayout(layout)
        return container

    def create_assignments_tab(self):
        layout = QVBoxLayout()

        # Dropdowns for assigning students and instructors
        form_layout = QFormLayout()
        self.course_dropdown = QComboBox()
        self.student_dropdown = QComboBox()
        self.instructor_dropdown = QComboBox()
        form_layout.addRow("Course:", self.course_dropdown)
        form_layout.addRow("Student:", self.student_dropdown)
        form_layout.addRow("Instructor:", self.instructor_dropdown)

        assign_button = QPushButton("Assign")
        assign_button.clicked.connect(self.assign_student_instructor)
        form_layout.addWidget(assign_button)

        # Button to refresh dropdowns
        refresh_button = QPushButton("Refresh Dropdowns")
        refresh_button.clicked.connect(self.refresh_dropdowns)
        layout.addWidget(refresh_button)

        layout.addLayout(form_layout)
        container = QWidget()
        container.setLayout(layout)
        return container

    def create_all_records_tab(self):
        # Create a table that displays all records (students, instructors, courses)
        self.all_records_table = QTableWidget(0, 5)
        self.all_records_table.setHorizontalHeaderLabels(["Type", "Name", "Age/Dept", "Email/Course Code", "Courses/Instructor"])
        self.refresh_all_records_table()

        layout = QVBoxLayout()
        layout.addWidget(self.all_records_table)
        container = QWidget()
        container.setLayout(layout)
        return container

    # Refresh table functions
    def refresh_students_table(self):
        self.students_table.setRowCount(0)
        for student in students:
            row_position = self.students_table.rowCount()
            self.students_table.insertRow(row_position)
            self.students_table.setItem(row_position, 0, QTableWidgetItem(student.name))
            self.students_table.setItem(row_position, 1, QTableWidgetItem(student.age))
            self.students_table.setItem(row_position, 2, QTableWidgetItem(student.email))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, r=row_position: self.delete_student(r))
            self.students_table.setCellWidget(row_position, 3, delete_button)

    def refresh_instructors_table(self):
        self.instructors_table.setRowCount(0)
        for instructor in instructors:
            row_position = self.instructors_table.rowCount()
            self.instructors_table.insertRow(row_position)
            self.instructors_table.setItem(row_position, 0, QTableWidgetItem(instructor.name))
            self.instructors_table.setItem(row_position, 1, QTableWidgetItem(instructor.department))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, r=row_position: self.delete_instructor(r))
            self.instructors_table.setCellWidget(row_position, 2, delete_button)

    def refresh_courses_table(self):
        self.courses_table.setRowCount(0)
        for course in courses:
            row_position = self.courses_table.rowCount()
            self.courses_table.insertRow(row_position)
            self.courses_table.setItem(row_position, 0, QTableWidgetItem(course.title))
            self.courses_table.setItem(row_position, 1, QTableWidgetItem(course.code))
            instructor_name = course.instructor.name if course.instructor else "No instructor"
            self.courses_table.setItem(row_position, 2, QTableWidgetItem(instructor_name))
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, r=row_position: self.delete_course(r))
            self.courses_table.setCellWidget(row_position, 3, delete_button)

    def refresh_all_records_table(self):
        self.all_records_table.setRowCount(0)
        for student in students:
            row_position = self.all_records_table.rowCount()
            self.all_records_table.insertRow(row_position)
            self.all_records_table.setItem(row_position, 0, QTableWidgetItem("Student"))
            self.all_records_table.setItem(row_position, 1, QTableWidgetItem(student.name))
            self.all_records_table.setItem(row_position, 2, QTableWidgetItem(student.age))
            self.all_records_table.setItem(row_position, 3, QTableWidgetItem(student.email))
            self.all_records_table.setItem(row_position, 4, QTableWidgetItem(", ".join(c.title for c in courses if student in c.students)))

        for instructor in instructors:
            row_position = self.all_records_table.rowCount()
            self.all_records_table.insertRow(row_position)
            self.all_records_table.setItem(row_position, 0, QTableWidgetItem("Instructor"))
            self.all_records_table.setItem(row_position, 1, QTableWidgetItem(instructor.name))
            self.all_records_table.setItem(row_position, 2, QTableWidgetItem(instructor.department))
            self.all_records_table.setItem(row_position, 3, QTableWidgetItem(""))
            self.all_records_table.setItem(row_position, 4, QTableWidgetItem(", ".join(c.title for c in courses if c.instructor == instructor)))

        for course in courses:
            row_position = self.all_records_table.rowCount()
            self.all_records_table.insertRow(row_position)
            self.all_records_table.setItem(row_position, 0, QTableWidgetItem("Course"))
            self.all_records_table.setItem(row_position, 1, QTableWidgetItem(course.title))
            self.all_records_table.setItem(row_position, 2, QTableWidgetItem(course.code))
            self.all_records_table.setItem(row_position, 3, QTableWidgetItem(""))
            self.all_records_table.setItem(row_position, 4, QTableWidgetItem(course.instructor.name if course.instructor else "No instructor"))

    # Add records functions
    def add_student(self):
        name = self.student_name_input.text()
        age = self.student_age_input.text()
        email = self.student_email_input.text()
        if name and age and email:
            students.append(Student(name, age, email))
            self.refresh_students_table()
            self.refresh_all_records_table()
            self.clear_student_form()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def add_instructor(self):
        name = self.instructor_name_input.text()
        department = self.instructor_department_input.text()
        if name and department:
            instructors.append(Instructor(name, department))
            self.refresh_instructors_table()
            self.refresh_all_records_table()
            self.clear_instructor_form()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def add_course(self):
        title = self.course_title_input.text()
        code = self.course_code_input.text()
        if title and code:
            courses.append(Course(title, code))
            self.refresh_courses_table()
            self.refresh_all_records_table()
            self.clear_course_form()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def assign_student_instructor(self):
        course_title = self.course_dropdown.currentText()
        student_name = self.student_dropdown.currentText()
        instructor_name = self.instructor_dropdown.currentText()

        course = next((c for c in courses if c.title == course_title), None)
        student = next((s for s in students if s.name == student_name), None)
        instructor = next((i for i in instructors if i.name == instructor_name), None)

        if course and student:
            if student not in course.students:
                course.students.append(student)
            self.refresh_all_records_table()
        else:
            QMessageBox.warning(self, "Assignment Error", "Invalid course or student.")

        if course and instructor:
            course.instructor = instructor
            self.refresh_courses_table()  # Refresh course table to update instructor information
            self.refresh_all_records_table()
        else:
            QMessageBox.warning(self, "Assignment Error", "Invalid course or instructor.")

    def refresh_dropdowns(self):
        self.course_dropdown.clear()
        self.student_dropdown.clear()
        self.instructor_dropdown.clear()

        self.course_dropdown.addItems([course.title for course in courses])
        self.student_dropdown.addItems([student.name for student in students])
        self.instructor_dropdown.addItems([instructor.name for instructor in instructors])

    def clear_student_form(self):
        self.student_name_input.clear()
        self.student_age_input.clear()
        self.student_email_input.clear()

    def clear_instructor_form(self):
        self.instructor_name_input.clear()
        self.instructor_department_input.clear()

    def clear_course_form(self):
        self.course_title_input.clear()
        self.course_code_input.clear()

    # Delete functions
    def delete_student(self, row):
        name = self.students_table.item(row, 0).text()
        global students
        students = [s for s in students if s.name != name]
        self.refresh_students_table()
        self.refresh_all_records_table()

    def delete_instructor(self, row):
        name = self.instructors_table.item(row, 0).text()
        global instructors
        instructors = [i for i in instructors if i.name != name]
        self.refresh_instructors_table()
        self.refresh_all_records_table()

    def delete_course(self, row):
        title = self.courses_table.item(row, 0).text()
        global courses
        courses = [c for c in courses if c.title != title]
        self.refresh_courses_table()
        self.refresh_all_records_table()

    # Export functions
    def export_students_to_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Age", "Email"])
                for student in students:
                    writer.writerow([student.name, student.age, student.email])

    def export_instructors_to_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Department"])
                for instructor in instructors:
                    writer.writerow([instructor.name, instructor.department])

    def export_courses_to_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Code", "Instructor"])
                for course in courses:
                    writer.writerow([course.title, course.code, course.instructor.name if course.instructor else "No instructor"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
