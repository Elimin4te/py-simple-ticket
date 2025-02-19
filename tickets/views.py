from flask import redirect, url_for, request
from flask.blueprints import Blueprint
from flask.views import MethodView
from flask.templating import render_template

from flask_login import current_user, login_required

from configuration import INDEX_URL, LOGIN_VIEW
from shared.views import render_into_index
from shared.menu import app_menu, MenuEntry

tickets_bp = Blueprint('tickets', __name__, template_folder='templates')

class IndexView(MethodView):

    decorators = [login_required]

    def get(self):
        content = ""
        return render_into_index(content, "Incidencias", "incidences")


tickets_bp.add_url_rule(
    INDEX_URL,
    view_func=IndexView.as_view(LOGIN_VIEW),
    methods=["GET"],
)

app_menu.add_entry(MenuEntry('incidences', 'Incidencias', 'fa-bell', INDEX_URL, 'soporte.incidencias', 10))
app_menu.add_entry(MenuEntry('tickets', 'Tickets', 'fa-wrench', INDEX_URL, 'soporte.tickets', 20))
app_menu.add_entry(MenuEntry('add_ticket', 'Crear Ticket', 'fa-plus', INDEX_URL, 'soporte.tickets', 30))
app_menu.add_entry(MenuEntry('activities', 'Actividades', 'fa-tasks', INDEX_URL, 'soporte.tickets.actividades', 40))

