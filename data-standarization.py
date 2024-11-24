import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from utils.db_utils import connect_to_database
import json

# Load configuration
with open('config.json') as f:
    config = json.load(f)

# Database connection
conn = connect_to_database(config['database'])

try:
    # Load data
    df = pd.read_sql('SELECT * FROM products', conn)
    print("Data for standardization:\n", df.head())

    # Normalize numerical columns
    numerical_columns = ['price', 'discount']  # Adjust columns as per dataset
    if any(col in df.columns for col in numerical_columns):
        scaler = MinMaxScaler()
        df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

    # Standardize categorical columns
    df['gender'] = df['gender'].str.title()
    df['masterCategory'] = df['masterCategory'].str.capitalize()
    # Normalize numerical columns (example: if you have numerical features)
    numerical_columns = ['column_name_1', 'column_name_2']  # Replace with actual column names
    scaler = MinMaxScaler()

    # Apply scaling only if the columns exist in the DataFrame
    for col in numerical_columns:
        if col in df.columns:
            df[col] = scaler.fit_transform(df[[col]])
            print(f"Normalized column: {col}")
    # Standardize categorical columns (example: lowercase all values in 'gender' column)
    categorical_columns = ['gender', 'masterCategory', 'subCategory']  # Replace with actual columns

    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].str.lower().str.strip()
            print(f"Standardized column: {col}")

    # Save standardized data
    df.to_sql('products', conn, if_exists='replace', index=False)

    print("Standardized Data:\n", df.head())
except Exception as e:
    print(f"Error during data standardization: {e}")
finally:
    conn.close()
    print("Data standardization complete.")
