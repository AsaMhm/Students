from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

class Student(BaseModel):
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
        raise HTTPException(status_code=500, detail=f"Failed to add student: {e}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
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


