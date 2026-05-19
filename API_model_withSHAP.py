from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import hash_password, verify_password, create_token
from pydantic import BaseModel
import pandas as pd
import joblib
import shap
from sklearn.preprocessing import LabelEncoder, StandardScaler
from database import SessionLocal
from model_table import DBStudent,DBTeacher
from auth import hash_password, verify_password, create_token, SECRET_KEY, ALGORITHM
from jose import jwt

app = FastAPI()

#for interaction of react app with my backend 
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('saved_model/xgb_model.pkl')
scaler = joblib.load('saved_model/scaler.pkl')
label_encoders = joblib.load('saved_model/label_encoders.pkl')

explainer = shap.TreeExplainer(model)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "failsafe_admin_2507"
# Protect helper moved up so it exists when used in Depends
def get_current_teacher(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
# --- REGISTER ---
class AdminLogin(BaseModel):
    username: str
    password: str
    
class TeacherRegister(BaseModel):
    username: str
    password: str

def verify_admin(credentials: AdminLogin):
    if credentials.username != ADMIN_USERNAME or \
       credentials.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Admin access denied")

@app.post('/admin/create-teacher')
def create_teacher(teacher: TeacherRegister, admin_user: str = Depends(get_current_teacher)):
    # Only works if logged in as admin
    if admin_user != ADMIN_USERNAME:
        raise HTTPException(status_code=403, detail="Admin access only")
    
    db = SessionLocal()
    existing = db.query(DBTeacher).filter(DBTeacher.username == teacher.username).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_teacher = DBTeacher(
        username=teacher.username,
        hashed_password=hash_password(teacher.password)
    )
    db.add(new_teacher)
    db.commit()
    db.close()
    return {"message": f"Teacher '{teacher.username}' created successfully"}
    
@app.post('/register')
def register(teacher: TeacherRegister):
    db = SessionLocal()
    existing = db.query(DBTeacher).filter(DBTeacher.username == teacher.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_teacher = DBTeacher(
        username=teacher.username,
        hashed_password=hash_password(teacher.password)
    )
    db.add(new_teacher)
    db.commit()
    db.close()
    return {"message": "Teacher registered successfully"}

# --- LOGIN ---
@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    teacher = db.query(DBTeacher).filter(DBTeacher.username == form_data.username).first()
    db.close()
    
    if not teacher or not verify_password(form_data.password, teacher.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token({"sub": teacher.username})
    return {"access_token": token, "token_type": "bearer"}

# --- PROTECT PREDICT ENDPOINT ---
def get_current_teacher(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


class Student(BaseModel):
    school: str
    sex: str
    age: int
    address: str
    famsize: str
    Pstatus: str
    Medu: int
    Fedu: int
    Mjob: str
    Fjob: str
    reason: str
    guardian: str
    traveltime: int
    studytime: int
    failures: int
    schoolsup: str
    famsup: str
    paid: str
    activities: str
    nursery: str
    higher: str
    internet: str
    romantic: str
    famrel: int
    freetime: int
    goout: int
    Dalc: int
    Walc: int
    health: int
    absences: int


@app.get('/')
def home():
    return {'message': 'FAILSAFE API Running'}

# Update predict to require login
@app.post('/predict')
def predict(student: Student, current_user: str = Depends(get_current_teacher)):
    data_dict = student.dict()
    
    # print("Columns received:", data_dict.keys())
    
    data_df = pd.DataFrame([data_dict])
    categorical_cols = ['school', 'sex', 'address', 'famsize', 'Pstatus',
                        'Mjob', 'Fjob', 'reason', 'guardian', 'schoolsup',
                        'famsup', 'paid', 'activities', 'nursery',
                        'higher', 'internet', 'romantic']
    
    # encode categorical columns
    for col in categorical_cols:
        if col in label_encoders:
            data_df[col] = label_encoders[col].transform(data_df[col])
        else:
            print(f"WARNING: No encoder found for column 'col'")

    # numeric_cols = ['age','Medu','Fedu','traveltime','studytime',
                    # 'failures','famrel','freetime','goout',
                    # 'Dalc','Walc','health','absences']    
    
    data_scaled= scaler.transform(data_df)

    prediction = model.predict(data_scaled)[0]
    probability = model.predict_proba(data_scaled)[0][1]

# shap index for risk class
    
    shap_values = explainer.shap_values(data_scaled)
    feature_names = list(data_df.columns)
    shap_vals = shap_values.tolist()[0]  # get first (only) row
    named_shap = dict(zip(feature_names, shap_vals))


# ---- SAVE TO DATABASE ---- #
    db = SessionLocal()
    db_record = DBStudent(
        age=data_dict['age'],
        school=data_dict['school'],
        sex=data_dict['sex'],
        studytime=data_dict['studytime'],
        failures=data_dict['failures'],
        absences=data_dict['absences'],
        higher=data_dict['higher'],
        internet=data_dict['internet'],
        famrel=data_dict['famrel'],
        goout=data_dict['goout'],
        predicted_risk=int(prediction),
        fail_probability=float(probability),
        shap_failures=named_shap.get('failures', 0),
        shap_absences=named_shap.get('absences', 0),
        shap_studytime=named_shap.get('studytime', 0),
        shap_goout=named_shap.get('goout', 0),
        shap_famrel=named_shap.get('famrel', 0),
        submitted_by=current_user
    )
    db.add(db_record)
    db.commit()
    db.close()
    # -------------------------- #
    
    return {
        'risk_prediction': int(prediction),
        'risk_probability': float(probability),
        'shap_values': named_shap   #for positive risk value we add [1]
    }