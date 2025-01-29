from flask import Flask
from flask_cors import CORS
from routes.user_routes import user_blueprint

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

app.register_blueprint(user_blueprint, url_prefix="/api/users")

if __name__ == "__main__":
    app.run(debug=True)
