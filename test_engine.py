from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

DATABASE_URL = 'postgresql://postgres:postgres2507@localhost/failsafe'

print("Initializing SQLAlchemy Engine...")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class DBStudentTest(Base):
    __tablename__ = "test_students"

    # Identity
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    name = Column(String)

    # Key Input Features
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

    # ML Output
    predicted_risk = Column(Integer)
    fail_probability = Column(Float)

    # Top SHAP Values
    shap_failures = Column(Float)
    shap_absences = Column(Float)
    shap_studytime = Column(Float)
    shap_goout = Column(Float)
    shap_famrel = Column(Float)

    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow)

try:
    print("\n[TEST A] Attempting to connect and create tables in PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("SUCCESS: Engine connected and 'test_students' table created!")

    print("\n[TEST B] Inserting mock ML risk record...")
    session = SessionLocal()

    mock_record = DBStudentTest(
        student_id="STU001",
        name="Test Student",
        age=18,
        school="GP",
        sex="F",
        studytime=1,
        failures=2,
        absences=20,
        higher="yes",
        internet="no",
        famrel=4,
        goout=4,
        predicted_risk=1,
        fail_probability=0.845,
        shap_failures=0.427,
        shap_absences=0.113,
        shap_studytime=-0.277,
        shap_goout=0.055,
        shap_famrel=-0.018
    )

    session.add(mock_record)
    session.commit()
    print("SUCCESS: Record inserted!")

    print("\n[TEST C] Querying data back from PostgreSQL...")
    retrieved_student = session.query(DBStudentTest).first()

    if retrieved_student:
        print("SUCCESS: Data read accurately!")
        print("---------------------------------------------")
        print(f"Student ID    : {retrieved_student.student_id}")
        print(f"Name          : {retrieved_student.name}")
        print(f"Absences      : {retrieved_student.absences}")
        print(f"Failures      : {retrieved_student.failures}")
        print(f"Risk Flag     : {retrieved_student.predicted_risk}")
        print(f"Probability   : {retrieved_student.fail_probability * 100:.1f}%")
        print(f"SHAP Failures : {retrieved_student.shap_failures}")
        print(f"SHAP Absences : {retrieved_student.shap_absences}")
        print("---------------------------------------------")

    print("\nCleaning up test records...")
    session.delete(retrieved_student)
    session.commit()
    session.close()
    print("Cleanup complete!")

except Exception as e:
    print(f"\nFAILED: {e}")