from shared.controllers.audited import AuditedModelController
from shared.controllers.mixins import DisableActionMixin
from auth.models.user import Usuario
from auth.controllers.role import RoleController, Rol

from datetime import datetime
from configuration.settings import TIMEZONE

from flask import request, render_template
from flask_login import login_required, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, ValidationError

from shared.views import ListView, FormView, handle_archiving
from shared.forms import required_string, DisabableFormMixin, format_obj_dates, assertion_catcher
from shared.engine import session

import bcrypt

USER_LIST_URL = '/users'
USER_ADD_URL = '/users/add'
USER_EDIT_URL = '/users/edit'


class UserController(AuditedModelController[Usuario], DisableActionMixin):

    model = Usuario
    model_pk_field = 'AF_alias'


    def hash_password(self, password: str) -> str:
        """ Hash the password using bcrypt with 16 rounds. """
        return bcrypt.hashpw(bytes(password, encoding='utf-8'), bcrypt.gensalt(16)).decode('utf-8')


    def try_password(self, instance: Usuario, password):
        """ Tries password for given user instance (False if the instance is None). """
        if instance:
            encoded_password = bytes(password, encoding='utf-8')
            hashed_password = bytes(instance.AF_contraseña, encoding='utf-8')
            return bcrypt.checkpw(encoded_password, hashed_password)

        return False


    def validate_password(self, password: str):

        assert len(password) >= 8, "La clave debe contener al menos 8 caracteres."
        assert any([char.isnumeric() for char in password]), "La clave debe contener al menos un número."
        assert any([char.isupper() for char in password]), "La clave debe contener al menos una letra mayúscula."
        assert all([char.isspace() == False for char in password]), "La clave no puede contener espacios."

        return password


    def change_password(self, instance, new_password: str):

        password = self.validate_password(new_password)
        password = self.hash_password(password)

        return self.update(instance, AF_contraseña=password)


    def create(
        self,
        AF_alias: str,
        AF_nombre: str,
        NU_cedula: int,
        AF_correo: str,
        AF_contraseña: str,
        AF_codigo_rol: str,
        AF_apellido: str = None,
        AF_correo_alternativo: str = None,
        AF_telefono_casa: str = None,
        AF_telefono_personal: str = None,
        **kwargs
    ):

        """ Validates the passed password and created an user. """

        password = self.validate_password(AF_contraseña)
        password = self.hash_password(password)
        
        instance = self.model(
            AF_alias = AF_alias,
            AF_nombre = AF_nombre,
            AF_apellido = AF_apellido,
            NU_cedula = NU_cedula,
            AF_correo = AF_correo,
            AF_contraseña = password,
            AF_codigo_rol = AF_codigo_rol,
            AF_correo_alternativo = AF_correo_alternativo,
            AF_telefono_casa = AF_telefono_casa,
            AF_telefono_personal = AF_telefono_personal
        )

        return super().create(instance)


@assertion_catcher
def validate_form_password(form, field):
    if field.data:
        UserController(session).validate_password(field.data)


class UserValidationForm(FlaskForm, DisabableFormMixin):
    AF_alias = required_string("Alias")
    AF_nombre = required_string("Nombre")
    AF_apellido = required_string("Apellido")
    NU_cedula = StringField("Cédula")
    AF_correo = required_string("Correo", Email("Proporcione un correo válido."))
    AF_contraseña = PasswordField("Clave", validators=[validate_form_password])
    AF_correo_alternativo = StringField("Correo Alternativo")
    AF_telefono_casa = StringField("Teléfono Casa")
    AF_telefono_personal = StringField("Teléfono Personal")
    AF_codigo_rol = required_string("Rol")
    AF_usuario_supervisor = StringField("Supervisor")


class UserListView(ListView):

    list_title = "Listado de Usuarios"
    page_title = "Usuarios"
    search_option_placeholder = "Buscar por alias..."
    active_menu_item = "users"
    controller = UserController(session)

    url = USER_LIST_URL

    def get_action_buttons_html(self) -> str:
        return render_template('user/action-buttons.html')

    def get_list_html(self) -> str:
        filter_set = {}
        filter_set['BO_activo'] = not ('BO_activo' in request.args)
        self.list_title = f'{self.list_title} {"(Inactivos)" if not filter_set["BO_activo"] else ""}' 

        search_str = request.args.get('search') or ''

        objects = self.controller.filter(
            Usuario.AF_alias.like('%' + search_str + '%'),
            order_by='TI_ultimo_inicio_sesion', 
            **filter_set
        )

        if len(objects) == 0:
            return None

        for obj in objects: 
            format_obj_dates(obj)

        return render_template(
            'user/list.html', objects=objects, edit_url=USER_EDIT_URL
        )


class UserCreateView(FormView):

    validation_form = UserValidationForm
    form_title = "Crear Usuario"
    page_title = "Usuarios"
    active_menu_item = "users"

    controller = UserController(session, current_user)
    url = USER_ADD_URL
    redirect_to = USER_LIST_URL

    def on_valid(self) -> None:
        creation_kwargs = {} | self.form_data
        creation_kwargs['NU_cedula'] = creation_kwargs['NU_cedula'].replace('.', '').strip()
        creation_kwargs.pop('BO_activo')
        self.controller.create(**creation_kwargs)

    def get_form_html(self) -> str:

        available_supervisors = ()
        if self.edit_mode:
            available_supervisors = UserController(session).filter(
                AF_codigo_rol="SPVS", BO_activo=True
            )

        roles = RoleController(session).filter(Rol.AF_codigo != 'ADM')

        return render_template(
            'user/form.html',
            edit_mode = self.edit_mode,
            obj = self.instance,
            supervisors = available_supervisors,
            roles = roles
        )


class UserEditView(UserCreateView):

    form_title = "Editar Usuario"

    edit_mode = True
    back_button = True
    url = USER_EDIT_URL
    redirect_to = USER_LIST_URL

    instance: Usuario = None

    def on_valid(self) -> None:

        updating_kwargs = {} | self.form_data
        updating_kwargs['NU_cedula'] = updating_kwargs['NU_cedula'].replace('.', '').strip()

        password = updating_kwargs.pop('AF_contraseña')
        if password:
            self.controller.change_password(self.instance, password)

        if updating_kwargs['AF_codigo_rol'] != 'ASPR':
            updating_kwargs['AF_usuario_supervisor'] = None

        self.controller.update(self.instance, **updating_kwargs)

    def get_helper_buttons_html(self) -> str:

        if self.instance.AF_codigo_rol == 'ASPR':
            list_tickets_url = f'/tickets?AF_analista_asignado={self.instance.AF_alias}'
            return render_template(
                'user/helper-buttons.html',
                list_tickets_url=list_tickets_url
            )

    def get_form_html(self) -> str:
        self.form_title = f'{self.form_title} - {self.instance.AF_alias}'
        return super().get_form_html()
