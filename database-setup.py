import pandas as pd
import sqlite3
import json
from utils.db_utils import connect_to_database, create_products_table

# Load configuration
with open('config.json') as f:
    config = json.load(f)

# Database connection and table creation
conn = connect_to_database(config['database'])
create_products_table(conn)

# Load dataset
try:
    data = pd.read_parquet('train-00000-of-00002-357f4cbabe1a8ea6.parquet')  # Adjust path as needed
    print("Loaded data:\n", data.head())
    print("Data types:\n", data.dtypes)
except Exception as e:
    print(f"Error loading dataset: {e}")
    conn.close()
    exit()

# Convert image column to bytes
data['image'] = data['image'].apply(
    lambda x: x['bytes'] if isinstance(x, dict) and 'bytes' in x else None
)

# Insert into database
try:
    data.to_sql('products', conn, if_exists='replace', index=False)
    print("Data inserted into database.")
except Exception as e:
    print(f"Error writing to database: {e}")
finally:
    conn.close()
