import psycopg2
from psycopg2 import sql

# Database connection details
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_USER = 'Boni'
DB_PASSWORD = 'boni3bolo3'
DB_NAME = 'CountyNavigator'

# Connect to the default postgres database to manage the target database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database='postgres'  # Connect to postgres to drop/create databases
)
conn.autocommit = True
cursor = conn.cursor()

# Terminate all connections to the database
cursor.execute("""
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = %s AND pid <> pg_backend_pid();
""", (DB_NAME,))

# Drop the database if it exists
cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(DB_NAME)))

# Create the database
cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))

# Close the connection
cursor.close()
conn.close()

print("Database reset complete.")
