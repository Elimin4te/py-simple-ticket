from flask import make_response, Response, Blueprint, Flask, redirect, request
from jinja2 import FileSystemLoader, Environment

from flask_login import current_user
from flask.views import MethodView
from flask_wtf import FlaskForm
from flask_wtf.csrf import generate_csrf

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
        'active_entry': app_menu.active_entry,
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
    active_menu_item: str = None,
    hide_search_bar: bool = False
):
    """ Renders a generic list view into the plain index. """

    context = {
        'list_title': list_title,
        'search_option_placeholder': search_option_placeholder,
        'action_buttons_html': action_buttons_html,
        'is_empty': is_empty,
        'list_html': html_content,
        'hide_search_bar': hide_search_bar
    }

    template = env.get_template('list-view.html')
    rendered_list = template.render(context)
    return render_into_index(
        rendered_list,
        page_title=page_title or list_title,
        active_menu_item=active_menu_item
    )


class View(MethodView):

    url: str = None
    methods: tuple = "GET",
    page_title: str = None
    active_menu_item: str = None
    """If declared, overrides the list_title attribute and sets a different navigator tab title."""

    def register_in_app(self, app: Blueprint | Flask):
        """ Register this view in the app url rules. """
        app.add_url_rule(
            rule=self.url,
            view_func=self.as_view(self.__class__.__name__.lower()),
            methods=self.methods
        )


class ListView(View):
    """Generic GET-only List View"""

    list_title: str
    list_html: str = None
    """If declared, overrides the get_list_html method."""
    search_option_placeholder: str = "Buscar por descripción..."
    action_buttons_html: str = None
    """If declared, overrides the get_action_buttons_html method."""
    hide_search_bar: bool = False
    force_empty: bool = False
    """If True, view will always be rendered in empty-search mode."""

    def get_list_html(self) -> str:
        """Inheritable method to stablish a way to dynamically obtain content html."""
        ...

    def get_action_buttons_html(self) -> str:
        """Inheritable method to stablish a way to dynamically obtain content html."""
        ...

    def render(self):
        """Resolves all methods and parameters and returns the rendered view. 

        If both, list_html and get_list_html are None, view will render in empty-search mode.
        """

        list_html = self.list_html or self.get_list_html()
        action_buttons = self.action_buttons_html or self.get_action_buttons_html()
        is_empty = True if self.force_empty else list_html is None
        return render_list_view(
            html_content=list_html,
            list_title=self.list_title,
            page_title=self.page_title,
            search_option_placeholder=self.search_option_placeholder,
            action_buttons_html=action_buttons,
            is_empty=is_empty,
            active_menu_item=self.active_menu_item,
            hide_search_bar=self.hide_search_bar
        )

    def get(self):
        return self.render()


def render_form_view(
    form_html: str,
    form_title: str,
    form_csrf: str,
    action_link: str = "#",
    back_to: str = None,
    helper_buttons_html: str = None,
    form_error: str = None,
    page_title: str = None,
    active_menu_item: str = None
):
    """ Renders a generic form view into the plain index. """

    context = {
        'form_title': form_title,
        'form_html': form_html,
        'helper_buttons_html': helper_buttons_html,
        'form_error': form_error,
        'form_csrf': form_csrf,
        'back_to': back_to,
        'action_link': action_link
    }

    template = env.get_template('form-view.html')
    rendered_form = template.render(context)
    return render_into_index(
        rendered_form,
        page_title=page_title or form_title,
        active_menu_item=active_menu_item
    )


class FormView(View):
    """Generic form get and post view with validation."""

    validation_form: FlaskForm
    """Used for validating the POST data."""

    form_title: str

    form_html: str = None
    """If declared, overrides the get_form_html method."""

    helper_buttons_html: str = None
    """HTML parsed helper buttons to display next to the form title."""

    action_link: str = "#"
    """Default form's action link."""

    form_data = None
    """Container for the form data which will be filled if the form is valid."""

    instanciated_form = None
    """Container for the form instance which will be filled when the post method is called."""

    redirect_to: str
    """Redirects to this url after the form is succesfully processed."""

    back_button: bool = False
    """Renders a button that redirects to self.redirect_to."""

    edit_mode: bool = False
    """Changes some behaviour if this form view is for editting."""

    instance: object = None
    """Instance state if this form is for editting."""

    controller: object = None
    """Controller class used for this view."""

    def get_instance(self) -> object | None:
        ...

    def on_valid(self) -> Response:
        """Inheritable method that executed an action when the form post was valid, should return a Response."""
        ...

    def get_form_html(self) -> str:
        """Inheritable method to stablish a way to dynamically obtain content html."""
        ...

    def get_helper_buttons_html(self) -> str:
        """Inheritable method to stablish a way to dynamically obtain helper buttons html."""
        ...

    def get_first_error(self, error_dict: dict[str, str]) -> str:
        """Returns the first error of the form errors as a string."""
        first_key = str(tuple(error_dict.keys())[0])
        first_label = getattr(self.instanciated_form, first_key).label
        err = error_dict[first_key]
        if isinstance(err, list):
            err = err[0]
        return f"{first_label}: {err}"

    def render(self, form_error: str = None):
        """Resolves all methods and parameters and returns the rendered view."""
        form_html = self.form_html or self.get_form_html()
        helper_buttons_html = self.helper_buttons_html or self.get_helper_buttons_html()
        assert form_html, "Form HTML content can't be empty."
        return render_form_view(
            form_html=form_html,
            back_to=self.redirect_to if self.back_button else None,
            helper_buttons_html=helper_buttons_html,
            form_title=self.form_title,
            form_csrf=generate_csrf(),
            form_error=form_error,
            action_link=self.action_link,
            page_title=self.page_title,
            active_menu_item=self.active_menu_item
        )

    def dispatch_request(self, **kwargs):

        if self.edit_mode:

            assert self.controller, "A controller is required for edit mode."
            assert self.redirect_to, "A redirect_to target is required for edit mode."

            if not request.args.get('_'):
                return redirect(self.redirect_to)

            self.instance = self.get_instance() or self.controller.get(request.args.get('_'))

        return super().dispatch_request(**kwargs)

    def get(self):
        return self.render()

    def post(self):

        form = self.validation_form()
        self.instanciated_form = form

        if form.validate():
            self.form_data: dict = form.data
            self.form_data.pop('csrf_token')
            self.on_valid()
            return redirect(self.redirect_to)

        form_error = self.get_first_error(form.errors)
        return self.render(form_error=form_error)


def handle_archiving(view_obj: View):

    set_archived = view_obj.form_data.get('BO_archivado')
    is_archived = view_obj.instance.BO_archivado

    # Set archiving date if archiving the object
    if not(set_archived == is_archived):

        reason = view_obj.form_data.pop('AF_motivo_archivado')

        if is_archived and not set_archived:
            view_obj.controller.unarchive_instance(view_obj.instance)

        if not is_archived and set_archived:
            view_obj.controller.archive_instance(view_obj.instance, reason)
