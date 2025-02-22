from shared.controllers.audited import AuditedModelController
from tickets.models import Prioridad

from flask import request, render_template, redirect
from flask_login import login_required, current_user

from flask_wtf import FlaskForm
from wtforms.validators import NumberRange

from shared.views import ListView, FormView
from shared.forms import CommonEntityFormMixin, required_string, required_int
from shared.engine import session

PRIORITY_EDIT_URL = '/priorities/edit'
PRIORITY_ADD_URL = '/priorities/add'
PRIORITY_LIST_URL = '/priorities'


class PriorityController(AuditedModelController[Prioridad]):
    
    model = Prioridad
    model_pk_field = 'AF_codigo'


# Remove unused attr making a class copy
PriorityCommonMixin = CommonEntityFormMixin
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

    def on_valid(self):
        instance = Prioridad(**self.form_data)
        self.controller.create(instance)
        return redirect(PRIORITY_LIST_URL)

    def get_form_html(self) -> str:
        return render_template("priority/form.html")


class PriorityEditView(PriorityCreateView):

    instance: Prioridad = None
    url = PRIORITY_EDIT_URL

    def get_instance(self):
        priority = request.args.get('_')
        priority = self.controller.get(priority)
        return priority

    def on_valid(self):
        priority = self.get_instance()
        self.controller.update(priority, **self.form_data)
        return redirect(PRIORITY_LIST_URL)

    def get_form_html(self) -> str:
        
        priority = self.get_instance()
        self.form_title = f"Editar Prioridad - {priority.AF_codigo}"
        return render_template(
            "priority/form.html", edit_mode=True, priority=priority
        )