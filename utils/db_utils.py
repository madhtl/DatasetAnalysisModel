import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        """
        Initialize the DatabaseManager with a database path.
        """
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """
        Establish a connection to the SQLite database.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            print(f"Connected to database at {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def create_products_table(self):
        """
        Create the products table if it doesn't already exist.
        """
        try:
            if self.conn is None:
                raise RuntimeError("Database connection not established.")
            cursor = self.conn.cursor()
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
            self.conn.commit()
            print("Products table created or already exists.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            raise

    def close(self):
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
