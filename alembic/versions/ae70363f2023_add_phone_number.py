"""add phone number

Revision ID: ae70363f2023
Revises: a7a9123d0c9a
Create Date: 2022-11-07 16:53:28.699840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae70363f2023'
down_revision = 'a7a9123d0c9a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column(
        'phone_number', sa.String(25), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
    pass
