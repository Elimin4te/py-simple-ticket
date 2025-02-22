from factory.alchemy import SQLAlchemyModelFactory
from tickets.models import Categoria

from shared.engine import session

class CategoryFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Categoria
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'
        sqlalchemy_get_or_create = ('AF_codigo',)


class AppCategoryFactory(CategoryFactory):

    AF_codigo = 'APP'
    AF_nombre = 'Aplicaciones'
    AF_descripcion = 'Fallos en aplicaciones'
    NU_nivel_jerarquia = 1


class GmailCategoryFactory(CategoryFactory):

    AF_codigo = 'GMAIL'
    AF_nombre = 'GMail'
    AF_descripcion = 'Fallos en GMail'
    AF_codigo_categoria_padre = 'APP'
    NU_nivel_jerarquia = 2


class ExcelCategoryFactory(CategoryFactory):

    AF_codigo = 'XLSX'
    AF_nombre = 'Excel'
    AF_descripcion = 'Fallos comunes de Excel'
    AF_codigo_categoria_padre = 'APP'
    NU_nivel_jerarquia = 2


class GmailCategoryFactory(CategoryFactory):

    AF_codigo = 'GDRIVE'
    AF_nombre = 'Google Drive'
    AF_descripcion = 'Fallos comunes de Google Drive'
    AF_codigo_categoria_padre = 'APP'
    NU_nivel_jerarquia = 2


class HWCategoryFactory(CategoryFactory):

    AF_codigo = 'HW'
    AF_nombre = 'Hardware'
    AF_descripcion = 'Fallos de Hardware'
    NU_nivel_jerarquia = 1


class PrinterCategoryFactory(CategoryFactory):

    AF_codigo = 'IMP'
    AF_nombre = 'Impresoras'
    AF_descripcion = 'Fallos de impresoras'
    AF_codigo_categoria_padre = 'HW'
    NU_nivel_jerarquia = 2


class ATSPrinterCategoryFactory(CategoryFactory):

    AF_codigo = 'IMP-TN'
    AF_nombre = 'Toner Defectuoso'
    AF_descripcion = 'Fallos de impresoras por toner defectuoso.'
    AF_codigo_categoria_padre = 'IMP'
    NU_nivel_jerarquia = 3
