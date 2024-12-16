Key Features:
Database Connection: The project connects to an SQLite database to load product data.
Data Preprocessing:
Non-numeric columns are dropped.
Categorical variables like 'masterCategory' and 'subCategory' are encoded using LabelEncoder.
Data is scaled using StandardScaler.
Model Training:
Three models (Logistic Regression, Random Forest, and SVM) are trained on the data.
The target column used for prediction is 'gender'.
Evaluation:
The models are evaluated based on accuracy, precision, recall, and F1 score.
A confusion matrix is generated for the Random Forest model, providing insight into classification performance.