import pandas as pd
import json
from utils.db_utils import connect_to_database, create_products_table
from utils.data_utils import transform_image_column

# Configuration
with open('config.json') as f:
    config = json.load(f)

# Connection to database
conn = connect_to_database(config['database'])

# Create products table
create_products_table(conn)

# Load and transform data
data = pd.read_parquet('train-00000-of-00002-357f4cbabe1a8ea6.parquet')
data = transform_image_column(data)

# Save data to database
data.to_sql('products', conn, if_exists='replace', index=False)
conn.close()

print("Database setup complete.")
