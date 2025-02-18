import psycopg2
from psycopg2 import Error
from config import Config


class Database:
    def create_connection():
        try:
            connection = psycopg2.connect(**Config.DATABASE)
            return connection
        except Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            return None
