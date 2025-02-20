from sqlalchemy.orm import Mapped, relationship
from typing import TypeAlias

from shared.database import (
    Base, 
    Id, generic_id, 
    CommonString, common_string, 
    CommonDatetime, common_datetime
)

from configuration.settings import UPLOADED_FILES_DIR


class DocumentoAdjunto(Base):

    __tablename__ = "DocumentosAdjuntos"

    NU_id: Id = generic_id()
    AF_nombre: CommonString = common_string(256)
    TI_fecha_creacion: CommonDatetime = common_datetime()

    @property
    def file_path(self):
        return UPLOADED_FILES_DIR / self.AF_nombre


RelatedDocuments: TypeAlias = Mapped[list[DocumentoAdjunto]]
related_documents = lambda relation_entity: relationship(secondary=relation_entity.__table__)