from shared.controllers.audited import AuditedModelController
from tickets.models import Prioridad

from flask import Response, render_template
from flask_login import login_required

from flask_wtf import FlaskForm
from wtforms.validators import NumberRange

from shared.views import ListView, FormView
from shared.forms import CommonEntityFormMixin, required_string, required_int


class PriorityController(AuditedModelController):
    
    model = Prioridad
    model_pk_field = 'AF_codigo'


class PriorityListView(ListView):
    decorators = [login_required]

    list_html = ""
    list_title = "Prioridades"
    active_menu_item = "priorities"
    force_empty = True
    hide_search_bar = True


class PriorityValidationForm(FlaskForm, CommonEntityFormMixin):
    colour = required_string()
    priority = required_int(NumberRange(1, 999, "La prioridad no puede ser menor de 1 ni mayor a 999."))


class PriorityCreateView(FormView):

    validation_form = PriorityValidationForm
    form_title = "Crear Prioridad"
    page_title = "Prioridades"
    active_menu_item = "priorities"

    def on_valid(self):
        return Response("Paso")

    def get_form_html(self) -> str:
        return render_template("priority/form.html")


