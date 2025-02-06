from shared.database import (
    Base, 
    ArchivableMixin, 
    Id, generic_id, 
    CommonString, common_string, 
    CommonDatetime, common_datetime
)


class Incidencia(Base, ArchivableMixin):

    __tablename__ = 'Incidencias'

    NU_incidencia: Id = generic_id()
    AF_titulo: CommonString = common_string(128)
    AF_descripcion: CommonString = common_string(5096)
    TI_fecha_creacion: CommonDatetime = common_datetime
    AF_nombre_reportador: CommonString = common_string(128)
    AF_correo_reportador: CommonString = common_string(128)

