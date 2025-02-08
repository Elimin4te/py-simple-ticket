from sqlalchemy import (
    orm,
    select,
    delete
)

from typing import TypeAlias

from shared.database import Base

_BaseDerivatedModel: TypeAlias = Base
_BaseDerivatedModelInstance: TypeAlias = Base

class BaseModelController:
    """ Abstract class for controlling a SQLALchemy Model operation. """

    def __init__(self, model_class: _BaseDerivatedModel, session: orm.Session = None) -> None:
        self.session = session
        self.model = model_class

    def assert_type(self, instance: _BaseDerivatedModelInstance):
        """ Checks the passed instance type to match the initialization passed model type. """
        assert type(instance) == type(self.model), "The passed instance doesn't matches the declared model for the controller."


class ReadController(BaseModelController):
    """ Basic read controller that allow for very basic operations. """

    def select(self):
        """ Returns a select statement for the controller's model. """
        return select(self.model)

    def all(self, *order_by):
        """ Shortcut function that reads all registries for the entity. """

        statement = self.select()
        if len(order_by):
            attrs = [getattr(self.model, attr) for attr in order_by]
            statement = statement.order_by(*attrs)
        return statement

    def filter(self, **criteria):
        """ Filter the registries using the specified criteria, such as id=123 or so. """

        return self.select().filter_by(**criteria)


class DeleteController(BaseModelController): # Inherits from read controller for filtering.
    """ Basic delete operation controller. """

    def delete(self, instance: _BaseDerivatedModelInstance):
        """ Deletes the passed instance. """

        self.assert_type(instance)

        self.session.add(instance)
        self.session.commit()
        return instance


class CreateController(BaseModelController):
    """ Basic create operation controller. """

    def create(self, instance: _BaseDerivatedModelInstance):
        """ Creates a registry based on the passed instance. """

        self.assert_type(instance)

        self.session.add(instance)
        self.session.commit()
        return instance


class UpdateController(BaseModelController):
    """ Basic update operation controller. """
        
    def update(self, instance: _BaseDerivatedModelInstance, **updating_fields):
        """ Updated attributes from the instance, saves it and returns the new instance. """

        self.assert_type(instance)

        for key, value in updating_fields.items():
            setattr(instance, key, value)

        self.session.commit()
        return instance


class ModelController(CreateController, ReadController, UpdateController, DeleteController):
    """ Mixin CRUD model controller. """

    model: _BaseDerivatedModel = None

    def __init__(self, session: orm.Session) -> None:
        super().__init__(self.model, session)

    