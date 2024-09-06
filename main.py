from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

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
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        grade INTEGER
        )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Database setup failed: {e}")

setup_database()

@app.get("/students")
async def get_students():
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()
        return {"students": students}
    except sqlite3.Error as e:
        logging.error(f"Failed to fetch students: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch students")

@app.post("/students")
async def add_student(student: Student):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (id, name, grade) VALUES (?, ?, ?)", (student.id, student.name, student.grade))
        conn.commit()
        conn.close()
        return {"message": "Student added successfully"}
    except sqlite3.IntegrityError:
        logging.error("Student with this ID already exists.")
        raise HTTPException(status_code=400, detail="Student with this ID already exists.")
    except sqlite3.Error as e:
        logging.error(f"Failed to add student: {e}")
        raise HTTPException(status_code=500, detail="Failed to add student")

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?", (student.name, student.grade, student_id))
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Student not found")
        conn.commit()
        conn.close()
        return {"message": "Student updated successfully"}
    except sqlite3.Error as e:
        logging.error(f"Failed to update student: {e}")
        raise HTTPException(status_code=500, detail="Failed to update student")

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Student not found")
        conn.commit()
        conn.close()
        return {"message": "Student deleted successfully"}
    except sqlite3.Error as e:
        logging.error(f"Failed to delete student: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete student")
