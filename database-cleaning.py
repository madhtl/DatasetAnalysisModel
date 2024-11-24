import pandas as pd
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
    print("Initial Data:\n", df.head())

    # Cleaning process
    df.fillna({'gender': 'Unknown', 'masterCategory': 'Other'}, inplace=True)
    df.drop_duplicates(inplace=True)
    df['id'] = df['id'].astype(str)

    # Save cleaned data
    df.to_sql('products', conn, if_exists='replace', index=False)

    # Summary
    print("Missing values after cleaning:\n", df.isnull().sum())
    print("Data types after cleaning:\n", df.dtypes)
    print("Duplicate rows after cleaning:", df.duplicated().sum())
except Exception as e:
    print(f"Error during data cleaning: {e}")
finally:
    conn.close()
    print("Data cleaning complete.")
