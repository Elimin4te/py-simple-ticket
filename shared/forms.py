from wtforms import StringField, IntegerField, Field
from wtforms.validators import DataRequired 

from shared.validators import code_validator, name_validator

def form_code_validator(form, field: Field):
    code_validator(field.data, field.name)

def form_name_validator(form, field: Field):
    name_validator(field.data, field.name)

required_string = lambda name, *validators: StringField(name, validators=[DataRequired(), *validators])
required_int = lambda name, *validators: IntegerField(name, validators=[DataRequired(), *validators])

class CommonEntityFormMixin:
    AF_codigo = required_string("Código", form_code_validator)
    AF_nombre = required_string("Nombre", form_name_validator)
    AF_descripcion = required_string("Descripción")