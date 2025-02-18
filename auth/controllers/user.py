from shared.controllers.audited import AuditedModelController
from shared.controllers.mixins import DisableActionMixin
from auth.models.user import Usuario

import bcrypt


class UserController(AuditedModelController[Usuario], DisableActionMixin):

    model = Usuario
    model_pk_field = 'AF_alias'


    def hash_password(self, password: str) -> str:
        """ Hash the password using bcrypt with 16 rounds. """
        return bcrypt.hashpw(bytes(password, encoding='utf-8'), bcrypt.gensalt(16)).decode('utf-8')


    def try_password(self, instance: Usuario, password):
        """ Tries password for given user instance (False if the instance is None). """
        if instance:
            hashed = self.hash_password(password)
            return instance.AF_contraseña == hashed

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
        alias: str,
        nombre: str,
        cedula: int,
        correo: str,
        contraseña: str,
        apellido: str = None,
        correo_alternativo: str = None,
        telefono_casa: str = None,
        telefono_personal: str = None,
    ):

        """ Validates the passed password and created an user. """

        password = self.validate_password(contraseña)
        password = self.hash_password(password)
        
        instance = self.model(
            AF_alias = alias,
            AF_nombre = nombre,
            AF_apellido = apellido,
            NU_cedula = cedula,
            AF_correo = correo,
            AF_contraseña = password,
            AF_correo_alternativo = correo_alternativo,
            AF_telefono_casa = telefono_casa,
            AF_telefono_personal = telefono_personal
        )

        return super().create(instance)