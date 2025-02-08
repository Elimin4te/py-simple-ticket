from shared.controllers.crud import ModelController, _BaseDerivatedModelInstance
from auth.models import Auditoria, Usuario


class AuditedModelController(ModelController):
    """ A CRUD operation mixin model where create, update and delete operations are recorded into an audit table. """

    model_pk_field: str = None
    """ Define the pk_field for the model to specify how the audit record will be created. """

    def __init__(self, session, user: Usuario) -> None:
        super().__init__(session)
        self.user = user


    def get_instance_pk(self, instance: _BaseDerivatedModelInstance):
        return getattr(instance, self.model_pk_field)


    def create(self, instance: _BaseDerivatedModelInstance):
        trace = Auditoria(
            AF_tabla=self.model.__tablename__,
            AF_accion="Crear",
            AF_id_registro=self.get_instance_pk(instance),
            AF_usuario_modificador=self.user.AF_alias
        )
        self.session.add(trace)

        return super().create(instance)


    def update(self, instance: _BaseDerivatedModelInstance, **updating_fields):
        for key, value in updating_fields.items():
            trace = Auditoria(
                AF_tabla=self.model.__tablename__,
                AF_accion="Modificar",
                AF_id_registro=self.get_instance_pk(instance),
                AF_campo_modificado=key,
                AF_valor_viejo=getattr(instance, key),
                AF_valor_nuevo=value,
                AF_usuario_modificador=self.user.AF_alias
            )
            self.session.add(trace)

        return super().update(instance, **updating_fields)


    def delete(self, instance: _BaseDerivatedModelInstance):
        trace = Auditoria(
            AF_tabla=self.model.__tablename__,
            AF_accion="Eliminar",
            AF_id_registro=self.get_instance_pk(instance),
            AF_usuario_modificador=self.user.AF_alias
        )
        self.session.add(trace)

        return super().delete(instance)