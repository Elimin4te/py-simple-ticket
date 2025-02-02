from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from shared.database import Base


class Role(Base):
    
    __tablename__ = 'Roles'

    code: Mapped[str] = mapped_column(
        String(4), 
        primary_key=True,
        name='AF_codigo'
    ) 

    name: Mapped[str] = mapped_column(
        String(16),
        name='AF_nombre'
    )

    description: Mapped[str] = mapped_column(
        String(128),
        name='AF_descripcion'
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True,
        name='BO_activo'
    )