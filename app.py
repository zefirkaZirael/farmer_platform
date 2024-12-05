from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import create_engine
from config import Config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)
    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:3000", "https://farmer-platform-v1.vercel.app"]}},
    )

    return app
