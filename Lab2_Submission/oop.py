import json
import re

# Person Class
class Person:
    def __init__(self, name, age, email):
        self.set_name(name)
        self.set_age(age)
        self.set_email(email)

    def introduce(self):
        return f"Hi, my name is {self.name}, and I am {self.age} years old."

    def get_email(self):
        return self._email

    def set_name(self, name):
        # Ensure name contains only letters and spaces
        if re.match(r"^[A-Za-z\s]+$", name):
            self.name = name
        else:
            raise ValueError("Invalid name. Name should only contain letters and spaces.")

    def set_age(self, age):
        # Ensure age is a positive integer
        if isinstance(age, int) and age > 0:
            self.age = age
        else:
            raise ValueError("Invalid age. Age must be a positive integer.")

    def set_email(self, email):
        # Basic email validation
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self._email = email
        else:
            raise ValueError("Invalid email format")


# Student Subclass
class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.set_student_id(student_id)
        self.registered_courses = []
    
    def set_student_id(self, student_id):
        # Validate student ID to start with 'S' and follow by digits
        if re.match(r"^S\d{4}$", student_id):
            self.student_id = student_id
        else:
            raise ValueError("Invalid student ID. It should start with 'S' followed by 4 digits.")

    def register_course(self, course):
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self.get_email(),
            "student_id": self.student_id,
            "registered_courses": [course.course_id for course in self.registered_courses]
        }

    @staticmethod
    def from_dict(data):
        return Student(data['name'], data['age'], data['email'], data['student_id'])


# Instructor Subclass
class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.set_instructor_id(instructor_id)
        self.assigned_courses = []
    
    def set_instructor_id(self, instructor_id):
        # Validate instructor ID to start with 'I' and follow by digits
        if re.match(r"^I\d{4}$", instructor_id):
            self.instructor_id = instructor_id
        else:
            raise ValueError("Invalid instructor ID. It should start with 'I' followed by 4 digits.")

    def assign_course(self, course):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self.get_email(),
            "instructor_id": self.instructor_id,
            "assigned_courses": [course.course_id for course in self.assigned_courses]
        }

    @staticmethod
    def from_dict(data):
        return Instructor(data['name'], data['age'], data['email'], data['instructor_id'])


# Course Class
class Course:
    def __init__(self, course_id, course_name):
        self.set_course_id(course_id)
        self.set_course_name(course_name)
        self.instructor = None
        self.enrolled_students = []

    def set_course_id(self, course_id):
        # Validate course ID to start with 'C' and follow by digits
        if re.match(r"^C\d{3}$", course_id):
            self.course_id = course_id
        else:
            raise ValueError("Invalid course ID. It should start with 'C' followed by 3 digits.")

    def set_course_name(self, course_name):
        # Ensure the course name is not empty
        if course_name.strip():
            self.course_name = course_name
        else:
            raise ValueError("Course name cannot be empty.")

    def add_student(self, student):
        self.enrolled_students.append(student)

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor": self.instructor.name if self.instructor else None,
            "enrolled_students": [student.student_id for student in self.enrolled_students]
        }

    @staticmethod
    def from_dict(data):
        return Course(data['course_id'], data['course_name'])


# Serialization
def save_to_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


def load_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)


# Example data (with valid inputs)
students = [
    Student("Alice Johnson", 20, "alice@example.com", "S1001"),
    Student("Bob Smith", 22, "bob@example.com", "S1002"),
]

courses = [
    Course("C101", "Math"),
    Course("C102", "Science")
]

instructors = [
    Instructor("Dr Smith", 45, "smith@example.com", "I1001"),
    Instructor("Dr Brown", 50, "brown@example.com", "I1002")
]

# Assign courses to instructors
instructors[0].assign_course(courses[0])  # Dr. Smith teaches Math
instructors[1].assign_course(courses[1])  # Dr. Brown teaches Science

# Register students for courses
students[0].register_course(courses[0])  # Alice registers for Math
students[1].register_course(courses[1])  # Bob registers for Science

# Save data to JSON files
save_to_file('students.json', [student.to_dict() for student in students])
save_to_file('instructors.json', [instructor.to_dict() for instructor in instructors])
save_to_file('courses.json', [course.to_dict() for course in courses])

# Create objects from the loaded data
def create_objects_from_data(students_data, instructors_data, courses_data):
    # Create course objects first
    course_map = {}
    for data in courses_data:
        course = Course.from_dict(data)
        course_map[course.course_id] = course
    
    # Create student and instructor objects
    student_map = {}
    instructor_map = {}
    
    for data in students_data:
        student = Student.from_dict(data)
        student_map[student.student_id] = student

    for data in instructors_data:
        instructor = Instructor.from_dict(data)
        instructor_map[instructor.instructor_id] = instructor
    
    # Set relationships for students and courses
    for student_data in students_data:
        student = student_map[student_data['student_id']]
        for course_id in student_data['registered_courses']:
            if course_id in course_map:
                student.register_course(course_map[course_id])
    
    # Set relationships for instructors and courses
    for instructor_data in instructors_data:
        instructor = instructor_map[instructor_data['instructor_id']]
        for course_id in instructor_data['assigned_courses']:
            if course_id in course_map:
                instructor.assign_course(course_map[course_id])
    
    return list(student_map.values()), list(instructor_map.values()), list(course_map.values())

# Load the data back from JSON files
students_data = load_from_file('students.json')
instructors_data = load_from_file('instructors.json')
courses_data = load_from_file('courses.json')

# Create objects and set relationships
loaded_students, loaded_instructors, loaded_courses = create_objects_from_data(students_data, instructors_data, courses_data)



# Testing the functionality with validations
try:
    invalid_student = Student("Invalid1Name", -5, "invalid_email", "1001")
except ValueError as e:
    print(f"Error: {e}")


# Valid input test
for student in loaded_students:
    print(student.introduce())
    print(f"Registered courses: {[course.course_name for course in student.registered_courses]}")
    print()

for instructor in loaded_instructors:
    print(instructor.introduce())
    print(f"Assigned courses: {[course.course_name for course in instructor.assigned_courses]}")
    print()



# Print out the loaded and linked data
print("Loaded Students and Registered Courses:")
for student in loaded_students:
    print(f"Student: {student.name}")
    registered_courses = [course.course_name for course in student.registered_courses]
    print(f"Registered courses: {', '.join(registered_courses) if registered_courses else 'None'}")

print("Loaded Instructors and Assigned Courses:")
for instructor in loaded_instructors:
    print(f"Instructor: {instructor.name}")
    assigned_courses = [course.course_name for course in instructor.assigned_courses]
    print(f"Assigned courses: {', '.join(assigned_courses) if assigned_courses else 'None'}")

print("Loaded Courses with Instructors and Enrolled Students:")
for course in loaded_courses:
    instructor_name = course.instructor.name if course.instructor else "None"
    enrolled_students = [student.name for student in course.enrolled_students]
    print(f"Course: {course.course_name}")
    print(f"Instructor: {instructor_name}")
    print(f"Enrolled students: {', '.join(enrolled_students) if enrolled_students else 'None'}")

