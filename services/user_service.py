from adapters.user_repository import UserRepository
from flask import jsonify


class UserService:

    def __init__(self):
        self.user_repo = UserRepository()

    def add_user(self, name, age):
        try:
            self.user_repo.insert_user(name, age)
            return jsonify({"message": "Usuario agregado exitosamente"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_all_users(self):
        try:
            users = self.user_repo.fetch_all_users()
            return jsonify({"results": users}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def search_users(self, name):
        try:
            users = self.user_repo.search_by_name(name)
            return jsonify({"results": users}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
