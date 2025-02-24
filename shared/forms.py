from wtforms import StringField, IntegerField, Field, BooleanField
from wtforms.validators import DataRequired, ValidationError

from shared.validators import code_validator, name_validator, length_validator

import dateparser

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


def get_common_entity_form_mixin():

    class CommonEntityFormMixin:
        AF_codigo = required_string("Código", form_code_validator)
        AF_nombre = required_string("Nombre", form_name_validator)
        AF_descripcion = required_string("Descripción")

    return CommonEntityFormMixin


class ArchivableFormMixin:
    BO_archivado = BooleanField("Archivado")
    AF_motivo_archivado = StringField("Motivo de Archivado", validators=[archiving_reason_validator])


class DisabableFormMixin:
    BO_activo = BooleanField("¿Activo?")


def format_obj_dates(obj: object, _format: str = '%Y-%m-%d %H:%M'):
    """Mutates an object for formatting it's dates attributes based of a given format."""
    time_attrs = tuple(filter(lambda k: k.startswith('TI_'), obj.__dict__.keys()))
    for attr in time_attrs:
        _old = getattr(obj, attr)
        # Assures it's not None
        if _old:
            # Assures it has the correct type
            if isinstance(_old, str):
                _old = dateparser.parse(_old)
            # Replace
            _new = _old.strftime(_format) 
            setattr(obj, attr, _new)


def sanitize_url_filter(model: object, request) -> dict:

    filter_set = {}
    for arg, val in request.args.items():
        if arg in model.__dict__:
            val = True if val == 'true' else False if val == 'false' else val
            filter_set[arg] = val

    return filter_set
