from documents.models import DocumentoAdjunto
from shared.controllers.audited import AuditedModelController

from fastapi import UploadFile
from configuration.settings import UPLOADED_FILES_DIR


class AttachedFileController(AuditedModelController):

    model = DocumentoAdjunto
    model_pk_field = 'NU_id'

    async def create(self, file: UploadFile):

        contents = await file.read()

        with open(UPLOADED_FILES_DIR/file.filename, 'wb') as f:
            f.write(contents)

        instance = self.model(AF_nombre=file.filename)

        return super().create(instance)
