import psycopg2
from psycopg2 import Error


DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "admin1",
    "host": "localhost",
    "port": 5433,
}


def create_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None
