import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier


# Read raw and clean manually
with open('student-mat.csv', 'r') as f:
    content = f.read()

# Remove the bad extra quotes
content = content.replace('""', '')
content = content.replace('"', '')

# Save cleaned version
with open('student-mat-clean.csv', 'w') as f:
    f.write(content)

# Now read clean file
df = pd.read_csv('student-mat-clean.csv', sep=';')
print(df.shape)
print(df.head())
print(df.isnull().sum())

# Data fixing
# # dropping rows is ending up in a shape of (0,33)
# df = df.dropna()                    # removes rows with missing values
# df = df.reset_index(drop=True)      # resets index after dropping
# print("Dataset shape:", df.shape)   # confirm data loaded correctly

# # Separate numeric and categorical columns
# numeric_cols = df.select_dtypes(include=['number']).columns
# categorical_cols = df.select_dtypes(include=['str', 'object']).columns

# # Fill numeric columns with MEDIAN
# for col in numeric_cols:
#     df[col] = df[col].fillna(df[col].median())

# # Fill categorical columns with MODE
# for col in categorical_cols:
#     df[col] = df[col].fillna(df[col].mode()[0])

# print("Missing values remaining:", df.isnull().sum().sum())  # should print 0

# Create risk column
df['risk'] = df['G3'].apply(lambda x: 1 if x < 10 else 0)

# Drop final grade

X = df.drop(['G1','G2','G3', 'risk'], axis=1)
y = df['risk']

# Encode categorical columns

label_encoders = {}

for col in X.select_dtypes(include=['str']).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le #keyed by column name

# Scale

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42
)

# Train model

model = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate

preds = model.predict(X_test)
print('Accuracy:', accuracy_score(y_test, preds))

# Save
import os
os.makedirs('saved_model', exist_ok=True)
joblib.dump(model, 'saved_model/xgb_model.pkl')
# joblib.dump(model, 'saved_model/xgb_model.pkl')
joblib.dump(scaler, 'saved_model/scaler.pkl')
joblib.dump(label_encoders, 'saved_model/label_encoders.pkl')