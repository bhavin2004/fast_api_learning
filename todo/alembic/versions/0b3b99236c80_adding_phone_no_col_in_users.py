"""adding phone no col in users

Revision ID: 0b3b99236c80
Revises: 
Create Date: 2025-08-18 19:01:31.320960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b3b99236c80'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column("phone_number",sa.String(),nullable=True,unique=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users",'phone_number')
