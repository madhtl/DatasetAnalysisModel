import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder, StandardScaler
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')  # Switch to TkAgg backend
import matplotlib.pyplot as plt
from utils.db_utils import connect_to_database

# Load configuration
with open('config.json') as f:
    config = json.load(f)

# Connect to the database and load data
conn = connect_to_database(config['database'])
df = pd.read_sql('SELECT * FROM products', conn)

# Display the first few rows to understand the data
print(df.head())

# Define the target column (let's assume we want to predict 'gender')
target_column = 'gender'

# Drop non-numeric or irrelevant columns
df = df.drop(columns=['filename', 'link', 'id', 'image'])  # Drop columns that aren't useful for the model

# Encode categorical variables using LabelEncoder
categorical_columns = ['masterCategory', 'subCategory']  # 'gender' is the target so it won't be encoded
label_encoder = LabelEncoder()

# Apply LabelEncoder for categorical columns
for col in categorical_columns:
    df[col] = label_encoder.fit_transform(df[col])

# Separate features (X) and target (y)
X = df.drop(target_column, axis=1)  # Features
y = df[target_column]  # Target

# Scale the features using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize the models
logreg = LogisticRegression(random_state=42, max_iter=200)  # Increased max_iter
rf = RandomForestClassifier(n_estimators=100, random_state=42)
svm = SVC(kernel='linear', random_state=42)

# Train models
logreg.fit(X_train, y_train)
rf.fit(X_train, y_train)
svm.fit(X_train, y_train)

# Function to evaluate a model
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average='weighted', zero_division=0)
    recall = recall_score(y_test, predictions, average='weighted', zero_division=0)
    f1 = f1_score(y_test, predictions, average='weighted', zero_division=0)
    return accuracy, precision, recall, f1

# Evaluate each model
logreg_metrics = evaluate_model(logreg, X_test, y_test)
rf_metrics = evaluate_model(rf, X_test, y_test)
svm_metrics = evaluate_model(svm, X_test, y_test)

# Print the evaluation results
print(f"Logistic Regression - Accuracy: {logreg_metrics[0]}, Precision: {logreg_metrics[1]}, Recall: {logreg_metrics[2]}, F1: {logreg_metrics[3]}")
print(f"Random Forest - Accuracy: {rf_metrics[0]}, Precision: {rf_metrics[1]}, Recall: {rf_metrics[2]}, F1: {rf_metrics[3]}")
print(f"SVM - Accuracy: {svm_metrics[0]}, Precision: {svm_metrics[1]}, Recall: {svm_metrics[2]}, F1: {svm_metrics[3]}")

# Confusion matrix for Random Forest
cm = confusion_matrix(y_test, rf.predict(X_test))

# Plot confusion matrix
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix for Random Forest')
plt.show()

# Create a comparison table for model performance
comparison = pd.DataFrame({
    'Model': ['Logistic Regression', 'Random Forest', 'SVM'],
    'Accuracy': [logreg_metrics[0], rf_metrics[0], svm_metrics[0]],
    'Precision': [logreg_metrics[1], rf_metrics[1], svm_metrics[1]],
    'Recall': [logreg_metrics[2], rf_metrics[2], svm_metrics[2]],
    'F1 Score': [logreg_metrics[3], rf_metrics[3], svm_metrics[3]]
})

# Print comparison table
print(comparison)
