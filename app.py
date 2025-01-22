import psycopg2
from flask import Flask, request, jsonify
import json
from database import create_connection
app = Flask(__name__)

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'admin1',
    'host': 'localhost',
    'port': 5433
}

@app.route('/api/users/', methods=['GET'])
def get_users():
    """Endpoint para obtener todos los usuarios."""
    try:
        diccionario = request.get_data()
        print("-----------------------------------________________________________________________________________")
        print(diccionario)
        print("-----------------------------------________________________________________________________________")
        
        a = json.loads(diccionario.decode('utf-8'))
        print("-----------------------------------________________________________________________________________")
        print(a)
        print("-----------------------------------________________________________________________________________")
        connection = create_connection(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO users (name, age) VALUES ('{a['name']}', {a['age']});")
        
        
        connection.commit()
        return jsonify('Correcto'), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/api/users/data', methods=['GET'])
def get_all_users():
    """Endpoint para obtener todos los usuarios de la base de datos."""
    try:
        connection = create_connection(**DB_CONFIG)
        cursor = connection.cursor()

        # Consultar todos los usuarios
        cursor.execute("SELECT id, name, age FROM users;")
        users = cursor.fetchall()

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


@app.route('/api/users/search', methods=['POST'])
def search_users():
    """Endpoint para buscar usuarios por nombre y edad."""
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        if not data or 'name'  not in data:
            return jsonify({'error': 'El cuerpo de la solicitud debe contener "name"'}), 400

        name = data['name']

        connection = create_connection(**DB_CONFIG)
        cursor = connection.cursor()

        # Consultar usuarios con coincidencia
        cursor.execute(f"SELECT id, name, age FROM users WHERE name = '{name}';")
        users = cursor.fetchall()

        if not users:
            return jsonify({'message': f'No se ha encontrado resultados con ese nombre: "{name}"',
                            'results': []})
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