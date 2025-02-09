from sqlalchemy import select

import re

def name_validator(name: str, field_name: str = None):
    """ Validate if a name is valid using simple criteria ."""
    title = "nombre" or field_name
    assert (2 < len(name) <= 64), f"El {title} no puede tener menos de 2 caracteres ni más de 64."
    assert re.match(r"^[a-zA-ZÀ-ÿ\s'-]+$", name) , f"El {title} no puede contener números ni símbolos."

    return name.strip()

def code_validator(code: str, field_name: str = None, check_for: str = "@#$%^&*¡!¿?=+-[]{}/\\"):

    title = "código" or field_name
    assert ' ' not in code, f"El {title} no puede contener espacios."
    assert all([char not in code for char in check_for]), f"El {title} no puede contener ninguno de estos caracteres: [{check_for}]."

    return code.strip()

def regex_validator(value: str, regex_pattern: str, field_name: str):

    pattern = re.compile(regex_pattern)
    assert re.match(pattern, value), f"El valor proporcionado para {field_name} no es válido."

    return value.strip()

def length_validator(value: str, lower: int, upper: int, field_name: str):

    assert lower <= len(value) <= upper, f"{field_name.capitalize()} debe tener al menos {lower} caracteres y máximo {upper}."
    
    return value.strip()