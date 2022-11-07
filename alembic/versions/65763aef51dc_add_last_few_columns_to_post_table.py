"""add last few columns to post table

Revision ID: 65763aef51dc
Revises: b061a707f02a
Create Date: 2022-11-07 16:50:31.726947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65763aef51dc'
down_revision = 'b061a707f02a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='1'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
