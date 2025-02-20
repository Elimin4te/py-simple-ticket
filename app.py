from flask import Flask, redirect
from flask_login import LoginManager

from configuration import settings, LOGIN_VIEW, INDEX_URL
from shared.engine import session
from shared.menu import Menu

from auth.controllers import UserController

from contextlib import suppress

from auth.views import auth_bp
from tickets.views import tickets_bp

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = settings.SECRET_KEY

login_manager = LoginManager(app)
login_manager.login_view = f"auth.{LOGIN_VIEW}"

@login_manager.user_loader
def load_user(alias: str):
    with suppress(Exception):
        return UserController(session).get(alias)

app.register_blueprint(auth_bp)
app.register_blueprint(tickets_bp)

app_menu = Menu()

@app.get('/')
def default_route():
    return redirect(INDEX_URL)



