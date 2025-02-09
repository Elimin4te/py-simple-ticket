from .document import DocumentoAdjunto, RelatedDocuments, related_documents
from .document_relation import (
    ArchivoAdjuntoIncidencia, 
    ArchivoAdjuntoTicket, 
    ArchivoAdjuntoTraza
)

__all__ = ["DocumentoAdjunto", "ArchivoAdjuntoIncidencia", "ArchivoAdjuntoTicket", "ArchivoAdjuntoTraza", "RelatedDocuments", "related_documents"]