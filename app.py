from flask import Flask, request, jsonify
from flask_cors import CORS
from decorators import db_connection
from repositories import UserRepository
from config import Config

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGIN}})

@app.route('/api/users/', methods=['POST'])
@db_connection
def create_user(cursor):
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({"error": "Required fields missing (name, age)"}), 400

    repo = UserRepository(cursor)
    repo.create(name, age)
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/users/data', methods=['GET'])
@db_connection
def get_all_users(cursor):
    repo = UserRepository(cursor)
    users = repo.get_all()
    
    if not users:
        return jsonify({'message': 'No users found', 'results': []}), 200

    return jsonify({'results': [user.to_dict() for user in users]}), 200

@app.route('/api/users/search', methods=['POST'])
@db_connection
def search_users(cursor):
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Request body must contain "name"'}), 400

    name = data['name'].split()[0]
    repo = UserRepository(cursor)
    users = repo.search_by_name(name)

    if not users:
        return jsonify({
            'message': f'No results found for name "{name}"',
            'results': []
        }), 200

    return jsonify({'results': [user.to_dict() for user in users]}), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@db_connection
def get_user(cursor, user_id):
    repo = UserRepository(cursor)
    user = repo.get_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)