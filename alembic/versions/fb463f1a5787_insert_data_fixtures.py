"""Insert data fixtures

Revision ID: fb463f1a5787
Revises: b08286f23ae1
Create Date: 2025-02-01 23:56:36.938562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import Session

from auth.models.fixtures.roles import (
    AdminRoleFactory,
    SupervisorRoleFactory,
    SupportRoleFactory
)

from auth.models.fixtures.users import DefaultAdminUserFactory

from auth.models.role import Role
from auth.models.user import User

from shared.engine import ENGINE


# revision identifiers, used by Alembic.
revision: str = 'fb463f1a5787'
down_revision: Union[str, None] = 'b08286f23ae1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = 'b08286f23ae1'

def upgrade() -> None:
    AdminRoleFactory()
    SupervisorRoleFactory()
    SupportRoleFactory()
    DefaultAdminUserFactory()


def downgrade() -> None:
    session = Session(ENGINE)
    session.query(User).filter_by(alias='admin').delete()
    session.query(Role).filter(Role.code.in_(["ADM", "SPVS", "ASPR"])).delete()
    session.commit()
    session.close()


