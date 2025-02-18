from functools import wraps
from database import Database
from flask import jsonify


def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = Database.create_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            connection.commit()
            return result
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            connection.close()

    return wrapper
