from shared.database import (
    Base, 
    Id, generic_id, 
    CommonString, common_string, 
    CommonDatetime, common_datetime
)


class DocumentoAdjunto(Base):

    __tablename__ = "DocumentosAdjuntos"

    id: Id = generic_id()
    AF_nombre: CommonString = common_string(256)
    TI_fecha_creacion: CommonDatetime = common_datetime()