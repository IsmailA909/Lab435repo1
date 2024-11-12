import sqlite3

def create_tables():
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('university.db')
    cursor = connection.cursor()
    
    # Create the students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # Create the instructors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    
    # Create the courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            code TEXT NOT NULL,
            instructor_id INTEGER,
            FOREIGN KEY (instructor_id) REFERENCES instructors(id)
        )
    ''')
    
    # Create the course_students table for enrollments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course_students (
            course_id INTEGER,
            student_id INTEGER,
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            PRIMARY KEY (course_id, student_id)
        )
    ''')
    
    # Commit changes and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
