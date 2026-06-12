from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from pydantic import BaseModel

from .database import Base, engine, get_db
from . import models

# Automatically build the database tables inside Postgres on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic validation schemas
class StudentBase(BaseModel):
    name: str
    reg_no: str
    email: str

class StudentResponse(StudentBase):
    id: int
    class Config:
        from_attributes = True

# 1. GET /health (Displays your registration number + DB status)
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "ok",
        "db": db_status,
        "student": "2212161"  # Your registration number explicitly linked here
    }

# 2. POST /students (Saves a new record to the database)
@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentBase, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.reg_no == student.reg_no).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Registration number already exists")
    
    new_student = models.Student(name=student.name, reg_no=student.reg_no, email=student.email)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# 3. GET /students (Returns all student records)
@app.get("/students", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# 4. GET /students/{reg_no} (Finds a specific student by registration number)
@app.get("/students/{reg_no}", response_model=StudentResponse)
def get_student_by_reg(reg_no: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.reg_no == reg_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found")
    return student