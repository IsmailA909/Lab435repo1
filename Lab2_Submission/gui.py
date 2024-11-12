import tkinter as tk
from tkinter import ttk, messagebox

# Mock Data for Courses and Students
courses_list = [
    {"course_id": "C101", "course_name": "Math"},
    {"course_id": "C102", "course_name": "Science"}
]

students_list = [
    {"name": "Alice Johnson", "age": 20, "email": "alice@example.com", "student_id": "S1001"},
    {"name": "Bob Smith", "age": 22, "email": "bob@example.com", "student_id": "S1002"}
]

instructors_list = [
    {"name": "Dr Smith", "age": 45, "email": "smith@example.com", "instructor_id": "I1001"},
    {"name": "Dr Brown", "age": 50, "email": "brown@example.com", "instructor_id": "I1002"}
]

# Step 1: Basic Window Setup
class SchoolManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("1000x600")

        self.tab_control = ttk.Notebook(root)
        
        self.student_tab = ttk.Frame(self.tab_control)
        self.instructor_tab = ttk.Frame(self.tab_control)
        self.course_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.student_tab, text='Students')
        self.tab_control.add(self.instructor_tab, text='Instructors')
        self.tab_control.add(self.course_tab, text='Courses')
        self.tab_control.pack(expand=1, fill="both")

        # GUI Components for each tab
        self.setup_student_form()
        self.setup_instructor_form()
        self.setup_course_form()
        self.display_records()

    def setup_student_form(self):
        # Student Form
        ttk.Label(self.student_tab, text="Student Name").grid(row=0, column=0, padx=10, pady=10)
        self.student_name_entry = ttk.Entry(self.student_tab)
        self.student_name_entry.grid(row=0, column=1)

        ttk.Label(self.student_tab, text="Age").grid(row=1, column=0, padx=10, pady=10)
        self.student_age_entry = ttk.Entry(self.student_tab)
        self.student_age_entry.grid(row=1, column=1)

        ttk.Label(self.student_tab, text="Email").grid(row=2, column=0, padx=10, pady=10)
        self.student_email_entry = ttk.Entry(self.student_tab)
        self.student_email_entry.grid(row=2, column=1)

        ttk.Label(self.student_tab, text="Student ID").grid(row=3, column=0, padx=10, pady=10)
        self.student_id_entry = ttk.Entry(self.student_tab)
        self.student_id_entry.grid(row=3, column=1)

        # Dropdown for courses
        ttk.Label(self.student_tab, text="Register for Course").grid(row=4, column=0, padx=10, pady=10)
        self.course_dropdown = ttk.Combobox(self.student_tab, values=[course['course_name'] for course in courses_list])
        self.course_dropdown.grid(row=4, column=1)

        # Button to Add Student
        ttk.Button(self.student_tab, text="Add Student", command=self.add_student).grid(row=5, column=0, columnspan=2, pady=10)

        # Treeview to Display Student Records
        self.student_tree = ttk.Treeview(self.student_tab, columns=("Name", "Age", "Email", "ID", "Courses"), show='headings')
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Age", text="Age")
        self.student_tree.heading("Email", text="Email")
        self.student_tree.heading("ID", text="Student ID")
        self.student_tree.heading("Courses", text="Courses")
        self.student_tree.grid(row=6, column=0, columnspan=2, pady=10)

    def setup_instructor_form(self):
        # Instructor Form
        ttk.Label(self.instructor_tab, text="Instructor Name").grid(row=0, column=0, padx=10, pady=10)
        self.instructor_name_entry = ttk.Entry(self.instructor_tab)
        self.instructor_name_entry.grid(row=0, column=1)

        ttk.Label(self.instructor_tab, text="Age").grid(row=1, column=0, padx=10, pady=10)
        self.instructor_age_entry = ttk.Entry(self.instructor_tab)
        self.instructor_age_entry.grid(row=1, column=1)

        ttk.Label(self.instructor_tab, text="Email").grid(row=2, column=0, padx=10, pady=10)
        self.instructor_email_entry = ttk.Entry(self.instructor_tab)
        self.instructor_email_entry.grid(row=2, column=1)

        ttk.Label(self.instructor_tab, text="Instructor ID").grid(row=3, column=0, padx=10, pady=10)
        self.instructor_id_entry = ttk.Entry(self.instructor_tab)
        self.instructor_id_entry.grid(row=3, column=1)

        # Dropdown for courses
        ttk.Label(self.instructor_tab, text="Assign Course").grid(row=4, column=0, padx=10, pady=10)
        self.assign_course_dropdown = ttk.Combobox(self.instructor_tab, values=[course['course_name'] for course in courses_list])
        self.assign_course_dropdown.grid(row=4, column=1)

        # Button to Add Instructor
        ttk.Button(self.instructor_tab, text="Add Instructor", command=self.add_instructor).grid(row=5, column=0, columnspan=2, pady=10)

        # Treeview to Display Instructor Records
        self.instructor_tree = ttk.Treeview(self.instructor_tab, columns=("Name", "Age", "Email", "ID", "Courses"), show='headings')
        self.instructor_tree.heading("Name", text="Name")
        self.instructor_tree.heading("Age", text="Age")
        self.instructor_tree.heading("Email", text="Email")
        self.instructor_tree.heading("ID", text="Instructor ID")
        self.instructor_tree.heading("Courses", text="Courses")
        self.instructor_tree.grid(row=6, column=0, columnspan=2, pady=10)

    def setup_course_form(self):
        # Course Form
        ttk.Label(self.course_tab, text="Course ID").grid(row=0, column=0, padx=10, pady=10)
        self.course_id_entry = ttk.Entry(self.course_tab)
        self.course_id_entry.grid(row=0, column=1)

        ttk.Label(self.course_tab, text="Course Name").grid(row=1, column=0, padx=10, pady=10)
        self.course_name_entry = ttk.Entry(self.course_tab)
        self.course_name_entry.grid(row=1, column=1)

        # Button to Add Course
        ttk.Button(self.course_tab, text="Add Course", command=self.add_course).grid(row=2, column=0, columnspan=2, pady=10)

        # Treeview to Display Course Records
        self.course_tree = ttk.Treeview(self.course_tab, columns=("ID", "Name"), show='headings')
        self.course_tree.heading("ID", text="Course ID")
        self.course_tree.heading("Name", text="Course Name")
        self.course_tree.grid(row=3, column=0, columnspan=2, pady=10)

    # Add Student and Register for Course
    def add_student(self):
        name = self.student_name_entry.get()
        age = self.student_age_entry.get()
        email = self.student_email_entry.get()
        student_id = self.student_id_entry.get()
        course_name = self.course_dropdown.get()
        
        if not name or not age or not email or not student_id:
            messagebox.showerror("Error", "All fields must be filled out")
            return
        
        courses = [course['course_id'] for course in courses_list if course['course_name'] == course_name]
        if courses:
            course_id = courses[0]
        else:
            course_id = "Not Registered"
        
        self.student_tree.insert('', 'end', values=(name, age, email, student_id, course_name))

    # Add Instructor and Assign to Course
    def add_instructor(self):
        name = self.instructor_name_entry.get()
        age = self.instructor_age_entry.get()
        email = self.instructor_email_entry.get()
        instructor_id = self.instructor_id_entry.get()
        course_name = self.assign_course_dropdown.get()
        
        if not name or not age or not email or not instructor_id:
            messagebox.showerror("Error", "All fields must be filled out")
            return
        
        courses = [course['course_id'] for course in courses_list if course['course_name'] == course_name]
        if courses:
            course_id = courses[0]
        else:
            course_id = "Not Assigned"
        
        self.instructor_tree.insert('', 'end', values=(name, age, email, instructor_id, course_name))

    # Add Course
    def add_course(self):
        course_id = self.course_id_entry.get()
        course_name = self.course_name_entry.get()
        
        if not course_id or not course_name:
            messagebox.showerror("Error", "All fields must be filled out")
            return
        
        self.course_tree.insert('', 'end', values=(course_id, course_name))

    # Display Records
    def display_records(self):
        # Clear existing records
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for item in self.instructor_tree.get_children():
            self.instructor_tree.delete(item)
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)

        # Insert mock data
        for student in students_list:
            self.student_tree.insert('', 'end', values=(student['name'], student['age'], student['email'], student['student_id'], "Math, Science"))

        for instructor in instructors_list:
            self.instructor_tree.insert('', 'end', values=(instructor['name'], instructor['age'], instructor['email'], instructor['instructor_id'], "Math"))

        for course in courses_list:
            self.course_tree.insert('', 'end', values=(course['course_id'], course['course_name']))

    # Search Functionality
    def search_records(self):
        search_query = self.search_entry.get().lower()
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for item in self.instructor_tree.get_children():
            self.instructor_tree.delete(item)
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        # Filter and re-insert records based on the search query
        for student in students_list:
            if search_query in student['name'].lower() or search_query in student['student_id'].lower():
                self.student_tree.insert('', 'end', values=(student['name'], student['age'], student['email'], student['student_id'], "Math, Science"))
        
        for instructor in instructors_list:
            if search_query in instructor['name'].lower() or search_query in instructor['instructor_id'].lower():
                self.instructor_tree.insert('', 'end', values=(instructor['name'], instructor['age'], instructor['email'], instructor['instructor_id'], "Math"))
        
        for course in courses_list:
            if search_query in course['course_name'].lower() or search_query in course['course_id'].lower():
                self.course_tree.insert('', 'end', values=(course['course_id'], course['course_name']))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementSystem(root)
    root.mainloop()
