from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configuration.settings import settings

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.get_database_url()

    db.init_app(app)

    return app