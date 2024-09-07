from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    grade: str

def create_table():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        grade TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup_event():
    create_table()
    
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
