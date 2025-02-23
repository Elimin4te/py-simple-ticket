from wtforms import StringField, IntegerField, Field, BooleanField
from wtforms.validators import DataRequired, ValidationError

from shared.validators import code_validator, name_validator, length_validator

def assertion_catcher(func):
    """ Decorator for making field validators based off assertion strategy. """

    def wrapper(*args, **kwargs):
        try: func(*args, **kwargs)
        except AssertionError as err: 
            raise ValidationError(str(err))

    return wrapper

@assertion_catcher
def form_code_validator(form, field: Field):
    code_validator(field.data, field.name)

@assertion_catcher
def form_name_validator(form, field: Field):
    name_validator(field.data, field.name)

@assertion_catcher
def archiving_reason_validator(form, field: Field):
    """Validates that there's a motive if archiving and also validates the motive length"""
    motive = form.AF_motivo_archivado.data
    has_motive = motive is not None and motive.strip() != ''

    if form.BO_archivado.data:
        assert has_motive, 'Se debe establecer un motivo de manera obligatoria al archivar.'
        length_validator(field.data, 32, 256, "El motivo de archivado")


required_string = lambda name, *validators: StringField(name, validators=[DataRequired(), *validators])
required_int = lambda name, *validators: IntegerField(name, validators=[DataRequired(), *validators])


class CommonEntityFormMixin:
    AF_codigo = required_string("Código", form_code_validator)
    AF_nombre = required_string("Nombre", form_name_validator)
    AF_descripcion = required_string("Descripción")


class ArchivableFormMixin:
    BO_archivado = BooleanField("Archivado")
    AF_motivo_archivado = StringField("Motivo de Archivado", validators=[archiving_reason_validator])
