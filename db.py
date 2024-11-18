import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the DATABASE_URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# Example usage of the connection
def example_query():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Example query
    cursor.execute("SELECT * FROM admin_credentials;")
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return results
