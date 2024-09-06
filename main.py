from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Student(BaseModel):
    id: int
    name: str
    grade: int

def setup_database():
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade INTEGER
        )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)
        # Adjust this part as it is not returning from a FastAPI endpoint
        return {"error": "FAILED to setup database"}

setup_database()

@app.get("/students")
async def get_students():
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()
        return students
    except sqlite3.Error as e:
        print(e)
        return {"error": "FAILED to fetch students"}

@app.post("/students")
async def add_student(student: Student):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (student.name, student.grade))
        conn.commit()
        conn.close()
        return {"message": "Student added successfully"}
    except sqlite3.Error as e:
        print(e)
        return {"error": "FAILED to add student"}

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?", (student.name, student.grade, student_id))
        conn.commit()
        conn.close()
        return {"message": "Student updated successfully"}
    except sqlite3.Error as e:
        print(e)
        return {"error": "FAILED to update student"}

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        return {"message": "Student deleted successfully"}
    except sqlite3.Error as e:
        print(e)
        return {"error": "FAILED to delete student"}


