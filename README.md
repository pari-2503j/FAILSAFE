# FAILSAFE
AI-powered student  risk prediction system using:
- FastAPI
- React
- XGBoost
- SHAP Explainability
SHAP is being used to predict indiuidual risk score. A positive value represents it's contribution towards increasing risk and a negative value represents how it helps reducing the risk and all these values are shown on the site while reviewing risk.FastAPI is being used to create connection between JWT authentication , database and frontend changes that cause changes in database.

## Features
- Teacher login authentication
- Admin panel for teacher creation
- Student risk prediction
- SHAP explainability
- Dashboard analytics

## Backend Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend Setup

```bash
npm install
npm start
```

if we login via admin as username and 'failsafe_admin_2507' as password, it logs into the admin page where it can check the risk of a student's failure along with add teachers who can login to check the risk stats. When a teacher logs in, it cannot add a teacher's credentials into the system but can check student failure risk stats and insert the data for which he/she wants to check student data for along with it recieve the possible intervention plans.
