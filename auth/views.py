from flask import redirect, request
from flask.blueprints import Blueprint
from flask.views import MethodView
from flask.templating import render_template

from flask_login import (
    current_user, 
    login_user, 
    login_required, 
    logout_user
)

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

from auth.controllers import UserController
from shared.engine import session
from shared.menu import app_menu, MenuEntry, MenuChild
from shared.views import ListView

from configuration import INDEX_URL

USER_LIST_URL = '/users'
USER_ADD_URL = '/users/add'

auth_bp = Blueprint('auth', __name__, template_folder='templates')


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Clave', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')


def render_login(form: LoginForm = None, **context):
    """ Shortcut function for rendering the login template. """
    form = form or LoginForm()
    return render_template('login.html', form=form, **context)


class LoginView(MethodView):

    def get_controller(self, user=None):
        return UserController(session, user)

    def get(self):

        if current_user.is_authenticated:
            return redirect(INDEX_URL)

        return render_login()

    def post(self):

        controller = self.get_controller()

        form_head_error = None
        form = LoginForm()

        if form.validate():

            user = controller.get(form.username.data)

            if not controller.try_password(user, form.password.data):
                form_head_error = "Credenciales Inválidas."

            if not form_head_error:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')

                if not next_page:
                    next_page = INDEX_URL

                return redirect(next_page)

        return render_login(form=form, form_head_error=form_head_error)


class LogoutView(MethodView):
    decorators = [login_required]

    def get(self):
        logout_user()
        return redirect('/login')


class UserListView(ListView):
    decorators = [login_required]

    list_html = ""
    list_title = "Listado de Usuarios"
    page_title = "Usuarios"
    search_option_placeholder= "Buscar por alias..."
    active_menu_item = "users"
    force_empty = True

    def get_controller(self, user=None):
        return UserController(session, user)



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

auth_bp.add_url_rule(
    "/users",
    view_func=UserListView.as_view("user-list-view"),
    methods=["GET"],
)

app_menu.add_entry(
    MenuEntry(
        'users', 
        'Gestionar Usuarios', 
        'fa-user', 
        breadcrumbs='autenticación.usuarios', 
        position=50,
        childs=(
            MenuChild("Listado", USER_LIST_URL),
            MenuChild("Crear", USER_ADD_URL)
        )
    )
)
