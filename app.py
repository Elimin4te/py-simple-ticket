from flask import Flask
from flask_login import LoginManager

from configuration.settings import settings
from shared.engine import session
from auth.controllers import UserController

from contextlib import suppress

from auth.views import auth_bp

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = settings.SECRET_KEY

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(alias: str):
    with suppress(Exception):
        return UserController(session).get(alias)

app.register_blueprint(auth_bp)



