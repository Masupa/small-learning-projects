from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()


class Student:
    """A class to represent a student"""
    def __init__(self, student_id, full_names, email, gender, course):
        self.student_id = student_id
        self.full_names = full_names
        self.email = email
        self.gender = gender
        self.course = course


class StudentBodyRequest(BaseModel):
    """A class to represent the student body request
    and to validate the data passed by the client to
    API"""
    student_id: Optional[int] = Field(description="An option student ID", default=None)
    full_names: str = Field(min_length=2, max_length=255)
    email: str = Field(min_length=10, max_length=255)
    gender: str = Field(min_length=4, max_length=10)
    course: str = Field(min_length=3, max_length=100)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "student_id": 1,
                    "full_names": "Sophia Wiggans",
                    "email": "swiggans0@unicef.org",
                    "gender": "Male",
                    "course": "Computer Science"
                }
            ]
        }
    }


STUDENTS = [
    Student(1, "Roddy Speed", "rspeed0@washington.edu", "Male", "Computer Science"),
    Student(2, "Theresa Yosevitz", "tyosevitz1@blogspot.com", "Female", "Business"),
    Student(3, "Ned Lamba", "nlamba2@t.co", "Male", "Economics"),
    Student(4, "Brianne Morgan", "bmorgan3@techcrunch.com", "Female", "Business"),
    Student(5, "Belia Drabble", "bdrabble4@sun.com", "Female", "Computer Science")
]


@app.get("/students", status_code=status.HTTP_200_OK)
async def read_students():
    """Fetch all students"""
    return STUDENTS


@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
async def read_student_by_id(student_id: int = Path(gt=0)):
    """Fetch a student given the student ID"""
    for student in STUDENTS:
        if student.student_id == student_id:
            return student
    raise HTTPException(
        status_code=404,
        detail=f"Student with student_id={student_id} is not found!"
    )


@app.get("/students/course/", status_code=status.HTTP_200_OK)
async def read_students_by_course(course_name: str = Query(min_length=3, max_length=100)):
    """Fetch all students enrolled in a particular course"""
    students_to_return = []
    for student in STUDENTS:
        if student.course.strip().lower() == course_name.strip().lower():
            students_to_return.append(student)
    return students_to_return


@app.get("/students/", status_code=status.HTTP_200_OK)
async def read_students_by_gender(gender: str = Query(min_length=4, max_length=10)):
    """Fetch all students of a given gender"""
    students_to_return = []
    for student in STUDENTS:
        if student.gender.strip().lower() == gender.strip().lower():
            students_to_return.append(student)
    return students_to_return


@app.post("/create-student", status_code=status.HTTP_201_CREATED)
async def create_student(new_student: StudentBodyRequest):
    """Create a new student"""
    student = Student(**new_student.model_dump())
    STUDENTS.append(find_student_id(student))


def find_student_id(student: Student):
    """Assign the next student_id to a student object"""
    if len(STUDENTS) == 0:
        student.student_id = 1
    else:
        student.student_id = STUDENTS[-1].student_id + 1
    return student


@app.put("/update-student", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(student_update: StudentBodyRequest):
    """Updates a student's details given a student ID"""
    student_updated = False
    for i, student in enumerate(STUDENTS):
        if student.student_id == student_update.student_id:
            STUDENTS[i] = student_update
            student_updated = True
            break
    if not student_updated:
        raise HTTPException(
            status_code=404,
            detail=f"Student with student_id={student_update.student_id} is not found!"
        )


@app.delete("/delete-student/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int = Path(gt=0)):
    """Removes an existing student given a student ID"""
    student_deleted = False
    for i, student in enumerate(STUDENTS):
        if student.student_id == student_id:
            STUDENTS.pop(i)
            student_deleted = True
            break
    if not student_deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Student with student_id={student_id} is not found!"
        )
