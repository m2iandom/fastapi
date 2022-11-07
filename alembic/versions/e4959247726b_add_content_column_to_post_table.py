"""add content column to post table

Revision ID: e4959247726b
Revises: aa5fc3f0a370
Create Date: 2022-11-07 16:46:36.738587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4959247726b'
down_revision = 'aa5fc3f0a370'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'content', sa.String(255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
