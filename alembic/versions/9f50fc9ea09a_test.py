"""test

Revision ID: 9f50fc9ea09a
Revises: 1128e975a763
Create Date: 2026-02-06 18:54:45.461391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f50fc9ea09a'
down_revision: Union[str, Sequence[str], None] = '1128e975a763'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
