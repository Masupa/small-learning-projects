from fastapi import FastAPI, Body


app = FastAPI()


STUDENTS = [
    {"student_id": 1, "full_names": "Roddy Speed", "email": "rspeed0@washington.edu", "gender": "Male", "course": "Computer Science"},
    {"student_id": 2, "full_names": "Theresa Yosevitz", "email": "tyosevitz1@blogspot.com", "gender": "Female", "course": "Business"},
    {"student_id": 3, "full_names": "Ned Lamba", "email": "nlamba2@t.co", "gender": "Male", "course": "Economics"},
    {"student_id": 4, "full_names": "Brianne Morgan", "email": "bmorgan3@techcrunch.com", "gender": "Female", "course": "Business"},
    {"student_id": 5, "full_names": "Belia Drabble", "email": "bdrabble4@sun.com", "gender": "Female", "course": "Computer Science"}
]


@app.get("/students")
async def read_students():
    """Fetch all students"""
    return STUDENTS


@app.get("/students/{student_id}")
async def read_student_by_id(student_id: int):
    """Fetch a student given the student ID"""
    for student in STUDENTS:
        if student['student_id'] == student_id:
            return student


@app.get("/students/course/")
async def read_students_by_course(course_name: str):
    """Fetch all students enrolled in a particular course"""
    students_to_return = []
    for student in STUDENTS:
        if student['course'].strip().lower() == course_name.strip().lower():
            students_to_return.append(student)
    return students_to_return


@app.get("/students/")
async def read_students_by_gender(gender: str):
    """Fetch all students of a given gender"""
    students_to_return = []
    for student in STUDENTS:
        if student['gender'].strip().lower() == gender.strip().lower():
            students_to_return.append(student)
    return students_to_return


@app.post("/create-student")
async def create_student(new_student=Body()):
    """Create a new student"""
    STUDENTS.append(new_student)


@app.put("/update-student")
async def update_student(student_update=Body()):
    """Updates a student's details given a student ID"""
    for i, student in enumerate(STUDENTS):
        if student['student_id'] == student_update['student_id']:
            STUDENTS[i] = student_update
            break


@app.delete("/delete-student/{student_id}")
async def delete_student(student_id: int):
    """Removes an existing student given a student ID"""
    for i, student in enumerate(STUDENTS):
        if student['student_id'] == student_id:
            STUDENTS.pop(i)
            break
