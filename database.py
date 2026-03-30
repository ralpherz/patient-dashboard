import psycopg2
import os

# Database configuration
# For first-time setup, update these values with your PostgreSQL credentials
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'patient_dashboard'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),  # Change this to your PostgreSQL password
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL is installed and running")
        print("2. The database 'patient_dashboard' exists")
        print("3. Your password in database.py is correct")
        print("\nTo create the database, run: python init_db.py")
        raise
