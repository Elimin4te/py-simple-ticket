from shared.controllers.crud import (
    ModelController, 
    _BaseDerivatedModelInstance, 
    T, Generic
)

from auth.models import Auditoria, Usuario

class AuditedModelController(ModelController[T], Generic[T]):
    """ A CRUD operation mixin model where create, update and delete operations are recorded into an audit table. """

    model_pk_field: str = None
    """ Define the pk_field for the model to specify how the audit record will be created. """

    def __init__(self, session, user: Usuario = None) -> None:
        super().__init__(session)
        self.user = user


    def get_instance_pk(self, instance: _BaseDerivatedModelInstance) -> str:
        return str(getattr(instance, self.model_pk_field))


    def validate_instance(func):
        
        def wrapped(self, *args, **kwargs):
            assert self.user, "La clase debe ser instanciada con un usuario para poder realizar esta operación."
            return func(self, *args, **kwargs)

        return wrapped

    @validate_instance
    def create(self, instance) -> T:
        
        trace = Auditoria(
            AF_tabla=self.model.__tablename__,
            AF_accion="Crear",
            AF_id_registro=self.get_instance_pk(instance),
            AF_usuario_modificador=self.user.AF_alias
        )
        self.session.add(trace)

        return super().create(instance)

    @validate_instance
    def update(self, instance: _BaseDerivatedModelInstance, **updating_fields) -> T:

        for key, value in updating_fields.items():

            old_value = getattr(instance, key)
            new_value = value
            if old_value == new_value: continue

            trace = Auditoria(
                AF_tabla=self.model.__tablename__,
                AF_accion="Modificar",
                AF_id_registro=self.get_instance_pk(instance),
                AF_campo_modificado=key,
                AF_valor_viejo=str(old_value),
                AF_valor_nuevo=str(new_value),
                AF_usuario_modificador=self.user.AF_alias
            )
            self.session.add(trace)

        return super().update(instance, **updating_fields)

    @validate_instance
    def delete(self, instance: _BaseDerivatedModelInstance) -> T:
        trace = Auditoria(
            AF_tabla=self.model.__tablename__,
            AF_accion="Eliminar",
            AF_id_registro=self.get_instance_pk(instance),
            AF_usuario_modificador=self.user.AF_alias
        )
        self.session.add(trace)

        return super().delete(instance)

    def get(self, pk) -> T:
        return super().get(pk)

    def all(self, *order_by) -> tuple[T]:
        return super().all(*order_by)

    def filter(self, *expression, order_by: str = None, **criteria) -> tuple[T]:
        return super().filter(*expression, order_by=order_by, **criteria)