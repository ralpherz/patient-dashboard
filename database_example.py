import psycopg2

# Database configuration
# Copy this file to database.py and update with your actual credentials
DB_CONFIG = {
    'dbname': 'patient_dashboard',
    'user': 'postgres',
    'password': 'YOUR_PASSWORD_HERE',  # Replace with your PostgreSQL password
    'host': 'localhost',
    'port': '5432'
}

def get_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        raise
