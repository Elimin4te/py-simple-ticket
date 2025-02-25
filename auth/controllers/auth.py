from datetime import datetime

from flask import redirect, request
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

from configuration import INDEX_URL, TIMEZONE


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Clave', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')


def render_login(form: LoginForm = None, **context):
    """ Shortcut function for rendering the login template. """
    form = form or LoginForm()
    return render_template('login.html', form=form, **context)


class LoginView(MethodView):

    def get_controller(self):
        return UserController(session, override=True)

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
                controller.update(user, TI_ultimo_inicio_sesion = datetime.now(TIMEZONE))
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
