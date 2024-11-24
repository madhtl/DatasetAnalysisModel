import pandas as pd
import json
from utils.db_utils import connect_to_database, update_product
from utils.data_utils import normalize_numerical_columns, standardize_categorical_columns

# Configuration
with open('config.json') as f:
    config = json.load(f)

# SQLite connection
conn = connect_to_database(config['database'])

# Load data from database
df = pd.read_sql('SELECT * FROM products', conn)
print("Initial Data: ")
print(df.head())

# Fill missing values
df.fillna({'gender': 'unknown', 'masterCategory': 'other'}, inplace=True)

# Standardize categorical data
df = standardize_categorical_columns(df, ['gender', 'masterCategory', 'subCategory'])

# Normalize numerical columns if applicable (replace with actual column names)
df = normalize_numerical_columns(df, ['numerical_column_1', 'numerical_column_2'])

# Remove duplicates
df.drop_duplicates(inplace=True)

# Save cleaned data back to the database
df.to_sql('products', conn, if_exists='replace', index=False)

conn.close()

print("Missing values after cleaning:", df.isnull().sum())
print("Duplicate rows after cleaning:", df.duplicated().sum())
print("Data cleaning complete.")
