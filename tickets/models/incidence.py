from shared.database import (
    Base, 
    ArchivableMixin, 
    Id, generic_id, 
    CommonString, common_string, 
    CommonDatetime, common_datetime
)

from documents.models import (
    ArchivoAdjuntoIncidencia, 
    RelatedDocuments, 
    related_documents
)

from contextlib import suppress


class Incidencia(Base, ArchivableMixin):

    __tablename__ = 'Incidencias'

    NU_incidencia: Id = generic_id(index=True)
    AF_titulo: CommonString = common_string(128, index=True)
    AF_descripcion: CommonString = common_string(5096)
    TI_fecha_creacion: CommonDatetime = common_datetime()
    AF_nombre_reportador: CommonString = common_string(128)
    AF_correo_reportador: CommonString = common_string(128)

    # ---- Attached Files
    documentos_adjuntos: RelatedDocuments = related_documents(ArchivoAdjuntoIncidencia)

    @property
    def has_ticket(self):

        ticket = False
        with suppress(Exception):
            ticket = getattr(self, 'ticket')
            ticket = bool(ticket)
        
        return ticket

    @property
    def associated_ticket_no(self):

        if self.has_ticket:
            return self.ticket[0].NU_ticket


        


