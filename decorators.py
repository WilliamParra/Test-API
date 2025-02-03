from database import create_connection
from functools import wraps  # Importamos wraps para mantener el nombre de la función original

def db_connection(func):
    @wraps(func)  # Esto evita el problema del nombre en Flask
    def wrapper(*args, **kwargs):
        connection = create_connection()
        if not connection:
            return {"error": "No se pudo conectar a la base de datos"}, 500

        cursor = connection.cursor()
        try:
            result = func(cursor, *args, **kwargs)  # Llamamos a la función original con `cursor`
            connection.commit()
            return result
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            connection.close()

    return wrapper
