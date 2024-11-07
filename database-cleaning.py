import pandas as pd
import sqlite3
import json

with open('config.json') as f:
    config = json.load(f)

# SQLite connection
conn = sqlite3.connect(config['database'])

df = pd.read_sql('SELECT * FROM products', conn)
print("Initial Data: ")
print(df.head())
print("Data types:", df.dtypes)

df.fillna({'gender': 'Unknown', 'masterCategory': 'Other'}, inplace=True)
df.drop_duplicates(inplace=True)
df['id'] = df['id'].astype(str)


df.to_sql('products', conn, if_exists='replace', index=False)

conn.close()

print("Missing values after cleaning:", df.isnull().sum())
print("Data types after cleaning:", df.dtypes)
print("Duplicate rows after cleaning:", df.duplicated().sum())

print("Data cleaning complete.")
