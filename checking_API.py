import requests

# The URL endpoint pointing to your local FastAPI server
url = "http://127.0.0.1:8000/predict"

# Step 1 - Register first
register = requests.post("http://127.0.0.1:8000/register", json={
    "username": "admin",
    "password": "failsafe_admin_2507"
})
print("Register response:", register.json())

# step2-login
login = requests.post("http://127.0.0.1:8000/login",data={
    "username":"teacher1",
    "password":"test123"
})
# print("Login response:", login.json())
# print("Login status code:", login.status_code)
# print("Login raw response:", login.text)

# Step 3 - Only proceed if login worked
if "access_token" not in login.json():
    print("LOGIN FAILED - stopping here")
    exit()
    
token = login.json()["access_token"]
# Mock data simulating a student profile 
# (High absences, low midterm grades to trigger a failure warning)
mock_student = {
    "school": "GP",
    "sex": "F",
    "age": 18,
    "address": "U",
    "famsize": "GT3",
    "Pstatus": "A",
    "Medu": 4,
    "Fedu": 4,
    "Mjob": "at_home",
    "Fjob": "teacher",
    "reason": "course",
    "guardian": "mother",
    "traveltime": 2,
    "studytime": 1,
    "failures": 2,
    "schoolsup": "yes",
    "famsup": "no",
    "paid": "no",
    "activities": "no",
    "nursery": "yes",
    "higher": "yes",
    "internet": "no",
    "romantic": "no",
    "famrel": 4,
    "freetime": 3,
    "goout": 4,
    "Dalc": 1,
    "Walc": 1,
    "health": 3,
    "absences": 20
}

# Post the data to the API
# Step 4 - Use token in predict
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(url, json=mock_student,headers=headers,timeout=60)
token = login.json()["access_token"]
# for actual error message from FastAPI
print(response.text)

# Print out the structured results returned by the API
if response.status_code == 200:
    result = response.json()
    print("--- API Test Success ---")
    print(f"Risk Prediction Flag: {result['risk_prediction']} (1 = Risk/Fail, 0 = Safe)")
    print(f"Risk Probability Confidence: {result['risk_probability'] * 100:.1f}%")
    print(f"SHAP Values Array Length: {len(result['shap_values'])}")
else:
    print(f"Failed to communicate. Status Code: {response.status_code}")