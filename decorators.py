from functools import wraps
from database import create_connection


def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = create_connection()
        if not connection:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        cursor = connection.cursor()
        try:
            result = func(cursor, connection, *args, **kwargs)
            return result
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            connection.close()

    return wrapper
