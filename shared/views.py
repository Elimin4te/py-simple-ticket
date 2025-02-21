from flask import make_response
from jinja2 import FileSystemLoader, Environment

from flask_login import current_user

from shared.menu import app_menu

template_loader = FileSystemLoader(searchpath="shared/templates")
env = Environment(loader=template_loader)

def render_into_index(rendered_template: str, page_title: str, active_menu_item: str = None):
    """ Renders the pierced html content rendered into the plain index menu as a HTMLResponse. """

    assert current_user.is_authenticated and not current_user.is_anonymous, (
        "Can't render into index menu for anonymous/unathenticated users."
    )

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


def render_list_view(
    html_content: str, 
    list_title: str,
    page_title: str = None,
    search_option_placeholder: str = "Buscar por descripción...",
    action_buttons_html: str = None,
    is_empty: bool = False,
    active_menu_item: str = None
):
    """ Renders a generic list view into the plain index. """

    context = {
        'list_title': list_title,
        'search_option_placeholder': search_option_placeholder,
        'action_buttons_html': action_buttons_html,
        'is_empty': is_empty,
        'list_html': html_content
    }

    template = env.get_template('list-view.html')
    rendered_list = template.render(context)
    return render_into_index(
        rendered_list, 
        page_title = page_title or list_title, 
        active_menu_item = active_menu_item
    )
