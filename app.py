import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from database import create_connection

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}}) # Permite solicitudes limitadas

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'admin1',
    'host': 'localhost',
    'port': 5433
}
@app.route('/api/users/', methods=['POST'])  # Change to POST
def get_users():
    try:
        data = request.get_json()  # Obtiene los datos JSON del cuerpo de la solicitud
        name = data.get('name')
        age = data.get('age')
        connection = create_connection(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
        
        connection.commit()
        return jsonify({"message": "User added successfully!"}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
        
@app.route('/api/users/data', methods=['GET'])
def get_all_users():
    """Endpoint para obtener todos los usuarios."""
    try:
        connection = create_connection(**DB_CONFIG)
        cursor = connection.cursor()

        # Consultar todos los usuarios
        cursor.execute("SELECT id, name, age FROM users;")
        users = cursor.fetchall()

        if not users:
            return jsonify({'message': 'No users found', 'results': []}), 200

        # Transformar los datos en formato JSON
        users_list = [{'id': user[0], 'name': user[1], 'age': user[2]} for user in users]
        
        return jsonify({'results': users_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.route('/api/users/search', methods=['POST'])
def search_users():
    """Endpoint para buscar usuarios por el primer nombre sin distinción entre mayúsculas y minúsculas."""
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        if not data or 'name' not in data:
            return jsonify({'error': 'El cuerpo de la solicitud debe contener "name"'}), 400

        name = data['name'].split()[0]  # Tomar solo la primera palabra del nombre ingresado

        connection = create_connection(**DB_CONFIG)
        cursor = connection.cursor()

        # Consultar usuarios comparando solo el primer nombre
        cursor.execute(
            """
            SELECT id, name, age 
            FROM users 
            WHERE LOWER(SPLIT_PART(name, ' ', 1)) = LOWER(%s);
            """, 
            (name,)
        )
        users = cursor.fetchall()

        if not users:
            return jsonify({
                'message': f'No se ha encontrado resultados con ese nombre: "{name}"',
                'results': []
            })

        # Transformar los datos en formato JSON
        users_list = [{'id': user[0], 'name': user[1], 'age': user[2]} for user in users]

        return jsonify(users_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()



# Endpoint para obtener un usuario por ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((item for item in data if item["id"] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404



if __name__ == '__main__':
    app.run(debug=True)