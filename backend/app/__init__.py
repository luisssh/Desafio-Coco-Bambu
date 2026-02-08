from flask import Flask
from flask_cors import CORS
from app.routes import routes
from app.models import init_db

def create_app():
    app = Flask(__name__)
    CORS(app)

    init_db()
    app.register_blueprint(routes)

    return app
