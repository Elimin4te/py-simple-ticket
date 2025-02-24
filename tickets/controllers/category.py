from shared.controllers.audited import AuditedModelController
from shared.controllers.mixins import DisableActionMixin

from tickets.models import Categoria

from flask import request, render_template, redirect
from flask_login import login_required, current_user

from wtforms import StringField
from flask_wtf import FlaskForm

from shared.views import ListView, FormView
from shared.forms import DisabableFormMixin, get_common_entity_form_mixin, sanitize_url_filter
from shared.engine import session

CATEGORY_LIST_URL = '/categories'
CATEGORY_ADD_URL = '/categories/add'
CATEGORY_EDIT_URL = '/categories/edit'

class CategoryController(AuditedModelController[Categoria], DisableActionMixin):
    
    model = Categoria
    model_pk_field = 'AF_codigo'

CategoryFormMixin = get_common_entity_form_mixin()

class CategoryValidationForm(FlaskForm, CategoryFormMixin, DisabableFormMixin):
    AF_codigo_categoria_padre = StringField("Categoría Padre")


class CategoryListView(ListView):
    decorators = [login_required]

    list_html = ""
    list_title = "Categorias"
    active_menu_item = "categories"
    hide_search_bar = True
    controller = CategoryController(session)

    url = CATEGORY_LIST_URL

    def get_action_buttons_html(self) -> str:
        return render_template('category/action-buttons.html')

    def get_list_html(self) -> str:

        filter_set = sanitize_url_filter(Categoria, request)
        if not 'BO_activo' in filter_set:
            filter_set['BO_activo'] = True

        else:
            self.list_title = f'{self.list_title} (Inactivas)'

        objects = self.controller.filter(order_by='NU_nivel_jerarquia', **filter_set)

        if len(objects) == 0:
            return None

        return render_template(
            'category/list.html', objects=objects, edit_url=CATEGORY_EDIT_URL
        )


class CategoryAddView(FormView):

    validation_form = CategoryValidationForm
    form_title = "Crear Categoría"
    page_title = "Categorías"
    active_menu_item = "categories"

    methods = "GET", "POST"
    controller = CategoryController(session, current_user)
    url = CATEGORY_ADD_URL
    redirect_to = CATEGORY_LIST_URL

    instance: Categoria = None

    def set_instance_hierarchy(self, instance):
        instance.NU_nivel_jerarquia = 1
        father = instance.categoria_padre
        while father:
            father = father.categoria_padre
            instance.NU_nivel_jerarquia += 1
        return instance.NU_nivel_jerarquia

    def on_valid(self):
        instance = Categoria(**self.form_data)
        self.set_instance_hierarchy(instance)
        self.controller.create(instance)

    def get_form_html(self) -> str:

        categories = ()
        obj = None
        if self.instance:
            obj = self.instance
            categories = self.controller.filter(
                Categoria.AF_codigo != self.instance.AF_codigo, BO_activo=True
            )
        else:
            categories = self.controller.filter(BO_activo=True)

        if len(categories) == 0:
            return None

        return render_template(
            'category/form.html', 
            edit_mode=self.edit_mode, 
            categories=categories,
            obj=obj
        )


class CategoryEditView(CategoryAddView):

    url = CATEGORY_EDIT_URL
    edit_mode = True
    back_button = True

    def on_valid(self):

        old_category = self.instance.AF_codigo_categoria_padre
        self.controller.update(self.instance, **self.form_data)
        new_category = self.instance.AF_codigo_categoria_padre

        if old_category != new_category:
            hierarchy_level = self.set_instance_hierarchy(self.instance)
            self.controller.update(self.instance, NU_nivel_jerarquia=hierarchy_level)

    def get_form_html(self) -> str:
        self.form_title = f'Editar Categoría - {self.instance.AF_nombre}'
        return super().get_form_html()