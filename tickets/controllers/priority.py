from shared.controllers.audited import AuditedModelController
from tickets.models import Prioridad

from flask import request, render_template, redirect
from flask_login import login_required, current_user

from flask_wtf import FlaskForm
from wtforms.validators import NumberRange

from shared.views import ListView, FormView
from shared.forms import get_common_entity_form_mixin, required_string, required_int
from shared.engine import session

from copy import copy

PRIORITY_EDIT_URL = '/priorities/edit'
PRIORITY_ADD_URL = '/priorities/add'
PRIORITY_LIST_URL = '/priorities'


class PriorityController(AuditedModelController[Prioridad]):
    
    model = Prioridad
    model_pk_field = 'AF_codigo'


# Remove unused attr making a class copy
PriorityCommonMixin = get_common_entity_form_mixin()
delattr(PriorityCommonMixin, 'AF_nombre')


class PriorityValidationForm(FlaskForm, PriorityCommonMixin):
    AF_color = required_string("Color")
    NU_prioridad = required_int(
        "Prioridad",
        NumberRange(1, 999, "La prioridad no puede ser menor de 1 ni mayor a 999.")
    )


class PriorityListView(ListView):
    decorators = [login_required]

    list_title = "Prioridades"
    active_menu_item = "priorities"
    hide_search_bar = True
    controller = PriorityController(session)

    url = PRIORITY_LIST_URL

    def get_list_html(self) -> str:
        priorities = self.controller.all('NU_prioridad')
        return render_template(
            'priority/list.html', priorities=priorities, edit_url=PRIORITY_EDIT_URL
        )


class PriorityCreateView(FormView):

    validation_form = PriorityValidationForm
    form_title = "Crear Prioridad"
    page_title = "Prioridades"
    active_menu_item = "priorities"

    methods = "GET", "POST"
    controller = PriorityController(session, current_user)
    url = PRIORITY_ADD_URL
    redirect_to = PRIORITY_LIST_URL

    def on_valid(self):
        instance = Prioridad(**self.form_data)
        self.controller.create(instance)

    def get_form_html(self) -> str:
        return render_template("priority/form.html")


class PriorityEditView(PriorityCreateView):

    instance: Prioridad = None
    url = PRIORITY_EDIT_URL
    edit_mode = True
    back_button = True

    def on_valid(self):
        self.controller.update(self.instance, **self.form_data)

    def get_form_html(self) -> str:
        self.form_title = f"Editar Prioridad - {self.instance.AF_codigo}"
        return render_template(
            "priority/form.html", edit_mode=True, priority=self.instance
        )