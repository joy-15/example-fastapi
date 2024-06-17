"""add last few columns to posts table

Revision ID: d827079eea47
Revises: ae5a1a8a62eb
Create Date: 2024-06-13 22:32:26.986297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd827079eea47'
down_revision: Union[str, None] = 'ae5a1a8a62eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable=True, server_default='TRUE'),
    )

    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('NOW()'),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
