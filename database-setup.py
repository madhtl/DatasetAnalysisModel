import pandas as pd
import sqlite3
import json

# Configuration
with open('config.json') as f:
    config = json.load(f)

# Connection->SQLite
conn = sqlite3.connect(config['database'])
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    filename TEXT,
    link TEXT,
    id TEXT,
    masterCategory TEXT,
    gender TEXT,
    subCategory TEXT,
    image BLOB
)
''')
conn.commit()

data = pd.read_parquet('train-00000-of-00002-357f4cbabe1a8ea6.parquet')  # Adjust path as needed

print(data.head())
print(data.dtypes)

# Need to convert image column from dictionary to bytes
data['image'] = data['image'].apply(lambda x: x['bytes'] if isinstance(x, dict) and 'bytes' in x else None)

data.to_sql('products', conn, if_exists='replace', index=False)
conn.close()

print("Database setup complete.")
