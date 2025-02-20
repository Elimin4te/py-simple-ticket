from sqlalchemy import (
    orm,
    select,
    delete
)

from typing import TypeAlias, Generic, TypeVar, Type

from shared.database import Base

_BaseDerivatedModelInstance: TypeAlias = Base
T = TypeVar("T")

class BaseModelController(Generic[T]):
    """ Abstract class for controlling a SQLALchemy Model operation. """

    model: Type[T] = None

    def __init__(self, session: orm.Session = None) -> None:
        self.session = session

    def assert_type(self, instance: _BaseDerivatedModelInstance):
        """ Checks the passed instance type to match the initialization passed model type. """
        assert type(instance) == self.model, f"The passed instance type ({type(instance)}) doesn't match the declared model for the controller ({self.model})."


class ReadController(BaseModelController):
    """ Basic read controller that allow for very basic operations. """

    def select(self):
        """ Returns a select statement for the controller's model. """
        return select(self.model)

    def get(self, pk) -> T:
        """ Gets one unique value from the model, if the pk_filter returns more than one value, an exception is risen. """
        return self.session.get(self.model, pk)

    def all(self, *order_by) -> tuple[T]:
        """ Shortcut function that reads all registries for the entity. """

        statement = self.select()
        if len(order_by):
            attrs = [getattr(self.model, attr) for attr in order_by]
            statement = statement.order_by(*attrs)

        return tuple(val[0] for val in self.session.execute(statement).unique())

    def filter(self, *args, **criteria) -> tuple[T]:
        """ Filter the registries using the specified criteria, where args is used for sqlalchemy field expressions and kwargs used for filter_by expressions. """

        return tuple(val[0] for val in self.session.execute(self.select().filter_by(**criteria).filter(*args)).unique())


class DeleteController(BaseModelController): # Inherits from read controller for filtering.
    """ Basic delete operation controller. """

    def delete(self, instance: _BaseDerivatedModelInstance) -> T:
        """ Deletes the passed instance. """

        self.assert_type(instance)

        self.session.add(instance)
        self.session.commit()
        return instance


class CreateController(BaseModelController):
    """ Basic create operation controller. """

    def create(self, instance: T) -> T:
        """ Creates a registry based on the passed instance. """

        self.assert_type(instance)

        self.session.add(instance)
        self.session.commit()
        return instance


class UpdateController(BaseModelController):
    """ Basic update operation controller. """
        
    def update(self, instance: _BaseDerivatedModelInstance, **updating_fields) -> T:
        """ Updated attributes from the instance, saves it and returns the new instance. """

        self.assert_type(instance)

        for key, value in updating_fields.items():
            setattr(instance, key, value)

        self.session.commit()
        return instance


class ModelController(CreateController, ReadController, UpdateController, DeleteController, Generic[T]):
    """ Mixin CRUD model controller. """

    def __init__(self, session: orm.Session) -> None:
        super().__init__(session)

    