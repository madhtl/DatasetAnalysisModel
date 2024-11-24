import sqlite3

def connect_to_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        print(f"Connected to database at {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise

def create_products_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            filename TEXT,
            link TEXT,
            id TEXT PRIMARY KEY,
            masterCategory TEXT,
            gender TEXT,
            subCategory TEXT,
            image BLOB
        )
        ''')
        conn.commit()
        print("Products table created or verified.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        raise

def update_product(conn, product_id, column, value):
    """
    Update a specific column in the products table for a given product ID.
    :param conn: SQLite connection object.
    :param product_id: ID of the product to update.
    :param column: Column name to update.
    :param value: New value for the column.
    """
    try:
        cursor = conn.cursor()
        query = f"UPDATE products SET {column} = ? WHERE id = ?"
        cursor.execute(query, (value, product_id))
        conn.commit()
        print(f"Updated product {product_id}: Set {column} to {value}")
    except sqlite3.Error as e:
        print(f"Error updating product: {e}")
