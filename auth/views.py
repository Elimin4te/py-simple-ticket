from flask import redirect, url_for, request
from flask.blueprints import Blueprint
from flask.views import MethodView
from flask.templating import render_template

from flask_login import current_user, login_user

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from auth.controllers import UserController
from shared.engine import session

auth_bp = Blueprint('auth', __name__, template_folder='templates')

class LoginView(MethodView):

    class LoginForm(FlaskForm):
        username = StringField('Usuario', validators=[DataRequired()])
        password = PasswordField('Clave', validators=[DataRequired()])
        remember_me = BooleanField('Recuérdame')

    @property
    def form(self):
        return self.LoginForm()

    def get_controller(self, user=None):
        return UserController(session, user)

    def get(self):

        if current_user.is_authenticated:
            return redirect(url_for('/'))

        return render_template('login.html', form=self.form)

    def post(self):

        controller = self.get_controller()

        if self.form.validate():

            user = controller.get(self.form.username.data)
            form_head_error = None

            if not controller.try_password(user, self.form.password.data):
                form_head_error = "Credenciales Inválidas."

            if not form_head_error:
                login_user(user, remember=self.form.remember_me.data)
                next_page = request.args.get('next')

                if not next_page:
                    next_page = url_for('/')

                return redirect(next_page)

        return render_template('login.html', form=self.form, form_head_error=form_head_error)


auth_bp.add_url_rule(
    "/login",
    view_func=LoginView.as_view("login-view"),
    methods=["GET", "POST"],
)

