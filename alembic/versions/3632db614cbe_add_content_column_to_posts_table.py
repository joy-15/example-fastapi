"""add content column to posts table

Revision ID: 3632db614cbe
Revises: 52e1caad0814
Create Date: 2024-06-13 21:56:36.849572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3632db614cbe'
down_revision: Union[str, None] = '52e1caad0814'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
