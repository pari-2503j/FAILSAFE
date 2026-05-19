from database import Base, engine
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

class DBStudent(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    name = Column(String)
    age = Column(Integer)
    school = Column(String)
    sex = Column(String)
    studytime = Column(Integer)
    failures = Column(Integer)
    absences = Column(Integer)
    higher = Column(String)
    internet = Column(String)
    famrel = Column(Integer)
    goout = Column(Integer)
    predicted_risk = Column(Integer)
    fail_probability = Column(Float)
    shap_failures = Column(Float)
    shap_absences = Column(Float)
    shap_studytime = Column(Float)
    shap_goout = Column(Float)
    shap_famrel = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    submitted_by= Column(String)
    pass

class DBTeacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    pass

#create tables
Base.metadata.create_all(bind=engine)