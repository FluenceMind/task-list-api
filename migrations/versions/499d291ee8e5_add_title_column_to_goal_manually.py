"""Add title column to goal manually

Revision ID: 499d291ee8e5
Revises: 7520b2ea5ed3
Create Date: 2025-11-17 01:07:37.471697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '499d291ee8e5'
down_revision = '7520b2ea5ed3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "goal",
        sa.Column("title", sa.String(), nullable=True),
    )


def downgrade():
    op.drop_column("goal", "title")
