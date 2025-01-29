from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_blueprint = Blueprint("user_routes", __name__)
user_service = UserService()


@user_blueprint.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")

    if not name or not age:
        return jsonify({"error": "Se requieren nombre y edad"}), 400

    return user_service.add_user(name, age)


@user_blueprint.route("/data", methods=["GET"])
def list_users():
    return user_service.get_all_users()


@user_blueprint.route("/search", methods=["POST"])
def search_user():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": 'El cuerpo de la solicitud debe contener "name"'}), 400

    return user_service.search_users(name)
