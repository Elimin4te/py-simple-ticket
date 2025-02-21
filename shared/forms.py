from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from shared.validators import code_validator, name_validator

required_string = lambda *validators: StringField(validators=[DataRequired(), *validators])
required_int = lambda *validators: IntegerField(validators=[DataRequired(), *validators])


class CommonEntityFormMixin:
    code = required_string(code_validator)
    name = required_string(name_validator)
    description = required_string()