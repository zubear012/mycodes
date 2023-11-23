from pathlib import Path
import mysql.connector
import os
from dotenv import *
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")

# MySQL database configuration
db_config = {
    'host': host,
    'user': user,
    'password': password,
    'database': database
}

# Function to establish a connection to the MySQL database
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Function to get a cursor from the database connection
def get_cursor(connection):
    return connection.cursor()
