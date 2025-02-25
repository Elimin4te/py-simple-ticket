from flask.blueprints import Blueprint

from auth.controllers.auth import LoginView, LogoutView
from auth.controllers.user import (
    UserListView,
    UserCreateView,
    UserEditView
)

from shared.menu import app_menu, MenuEntry, MenuChild


auth_bp = Blueprint('auth', __name__, template_folder='templates')

auth_bp.add_url_rule(
    "/login",
    view_func=LoginView.as_view("login-view"),
    methods=["GET", "POST"],
)

auth_bp.add_url_rule(
    "/logout",
    view_func=LogoutView.as_view("logout-view"),
    methods=["GET", "POST"],
)

UserListView().register_in_app(auth_bp)
UserEditView().register_in_app(auth_bp)
UserCreateView().register_in_app(auth_bp)

app_menu.add_entry(
    MenuEntry(
        'users', 
        'Gestionar Usuarios', 
        'fa-user', 
        breadcrumbs='autenticación.usuarios', 
        position=100,
        childs=(
            MenuChild("Listado", UserListView.url),
            MenuChild("Crear", UserCreateView.url)
        )
    )
)
