from flask import make_response
from jinja2 import FileSystemLoader, Environment

from flask_login import current_user

from shared.menu import app_menu

def render_into_index(rendered_template: str, page_title: str, active_menu_item: str = None):
    """ Renders the pierced html content rendered into the main index menu as a HTMLResponse. """

    assert current_user.is_authenticated and not current_user.is_anonymous, (
        "Can't render into index menu for anonymous/unathenticated users."
    )

    template_loader = FileSystemLoader(searchpath="shared/templates")
    env = Environment(loader=template_loader)
    template = env.get_template('index.html')

    if active_menu_item:
        app_menu.set_entry_active(active_menu_item)

    context = {
        'content': rendered_template, 
        'title': page_title, 
        'user': current_user,
        'menu': app_menu,
        'active_entry': app_menu.active_entry
    }

    output = template.render(context)

    return make_response(output)