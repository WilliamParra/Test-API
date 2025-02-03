from flask import Flask, request, jsonify
from flask_cors import CORS
from decorators import db_connection

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

@app.route('/api/users/', methods=['POST'])
@db_connection
def create_user(cursor):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({"error": "Faltan datos requeridos (name, age)"}), 400

    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    return jsonify({"message": "User added successfully!"}), 201

@app.route('/api/users/data', methods=['GET'])
@db_connection
def get_all_users(cursor):
    cursor.execute("SELECT id, name, age FROM users;")
    users = cursor.fetchall()

    if not users:
        return jsonify({'message': 'No users found', 'results': []}), 200

    users_list = [{'id': u[0], 'name': u[1], 'age': u[2]} for u in users]
    return jsonify({'results': users_list}), 200

@app.route('/api/users/search', methods=['POST'])
@db_connection
def search_users(cursor):
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'El cuerpo de la solicitud debe contener "name"'}), 400

    name = data['name'].split()[0]  # Tomar solo la primera palabra del nombre ingresado

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
        return jsonify({'message': f'No se encontraron resultados con el nombre "{name}"', 'results': []}), 200

    users_list = [{'id': u[0], 'name': u[1], 'age': u[2]} for u in users]
    return jsonify({'results': users_list}), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@db_connection
def get_user(cursor, user_id):
    cursor.execute("SELECT id, name, age FROM users WHERE id = %s;", (user_id,))
    user = cursor.fetchone()

    if user:
        return jsonify({'id': user[0], 'name': user[1], 'age': user[2]}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
