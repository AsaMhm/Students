from fastapi import FastApi

from pydantic import BaseModel

import sqlite3

app = FastApi()

class Student(BaseModel):

id:int

name:str

grade:int

def setup_database ():

try:

conn = sqlite3.connect("students.db")

curser = conn.cursor()

curser.execute('''

CREATE TABLE IF NOT EXISTS students(

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT NOT NULL,

grade INTEGER

)

''')

conn.commit()

except sqlite3.Error as e:

print(e)

return {"error":"FIELED to fetch students"}

setup_database()

@app.get("students")

async def getStudents():

try:

conn = sqlite3.connect("students.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM students")

students = cursor.fetchall()

conn.close()

return students

except sqlite3.Error as e:

print(e)

return {"error":"FIELED to read students"}

@app.post("students")

async def addStudent(student:Student):

try:

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name,grade) VALUES(?,?)",(student.name,student.grade))
    conn.commit()
    conn.close()
    return {"message":"student add congratiolation"}
except sqlite3.Error as e:

print(e) 

return {"error":"FIELED to add student"}

@app.put("students/{student_id}")

async def update_students(student_id:int,student:Student):

try:

conn = sqlite3.connect("students.db")

cursor = conn.cursor()

cursor.execute("UPDATE students SET name = ?,grade = ? WHERE id=?",(student.name,student.grade,student_id))

conn.commit()

conn.close()

return {"message":"Update student congratolation"}

except sqlite3.Error as e:

print(e)

return {"error":"FIELED to update student"}

@app.delete("students/{student_id}")

async def delete_student(student_id:int):

try: 

conn = sqlite3.connect("students.db")

cursor = conn.cursor()

cursor.execute("DELETE FROM students WHERE id =?",(student_id))

conn.commit()

conn.close()

return {"message":"delete student congratolation"}

except sqlite3.Error as e:

print(e)

return {"error":"FIELED to delete student"}
