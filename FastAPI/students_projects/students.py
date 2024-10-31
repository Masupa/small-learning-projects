from fastapi import FastAPI, Body


app = FastAPI()


class Student:
    """A class to represent a student"""
    student_id: int
    full_names: str
    email: str
    gender: str
    course: str

    def __init__(self, student_id, full_names, email, gender, course):
        self.student_id = student_id
        self.full_names = full_names
        self.email = email
        self.gender = gender
        self.course = course


STUDENTS = [
    Student(1, "Roddy Speed", "rspeed0@washington.edu", "Male", "Computer Science"),
    Student(2, "Theresa Yosevitz", "tyosevitz1@blogspot.com", "Female", "Business"),
    Student(3, "Ned Lamba", "nlamba2@t.co", "Male", "Economics"),
    Student(4, "Brianne Morgan", "bmorgan3@techcrunch.com", "Female", "Business"),
    Student(5, "Belia Drabble", "bdrabble4@sun.com", "Female", "Computer Science")
]


@app.get("/students")
async def read_students():
    """Fetch all students"""
    return STUDENTS


@app.get("/students/{student_id}")
async def read_student_by_id(student_id: int):
    """Fetch a student given the student ID"""
    for student in STUDENTS:
        if student.student_id == student_id:
            return student


@app.get("/students/course/")
async def read_students_by_course(course_name: str):
    """Fetch all students enrolled in a particular course"""
    students_to_return = []
    for student in STUDENTS:
        if student.course.strip().lower() == course_name.strip().lower():
            students_to_return.append(student)
    return students_to_return


@app.get("/students/")
async def read_students_by_gender(gender: str):
    """Fetch all students of a given gender"""
    students_to_return = []
    for student in STUDENTS:
        if student.gender.strip().lower() == gender.strip().lower():
            students_to_return.append(student)
    return students_to_return


@app.post("/create-student")
async def create_student(new_student=Body()):
    """Create a new student"""
    student = Student(**new_student)
    STUDENTS.append(student)


@app.put("/update-student")
async def update_student(student_update=Body()):
    """Updates a student's details given a student ID"""
    for i, student in enumerate(STUDENTS):
        if student.student_id == student_update['student_id']:
            STUDENTS[i] = student_update
            break


@app.delete("/delete-student/{student_id}")
async def delete_student(student_id: int):
    """Removes an existing student given a student ID"""
    for i, student in enumerate(STUDENTS):
        if student.student_id == student_id:
            STUDENTS.pop(i)
            break
