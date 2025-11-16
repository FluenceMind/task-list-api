"""Wave 6: add goal_id FK to tasks

Revision ID: 85a867a6bac3
Revises: 9633754af3cf
Create Date: 2025-11-15 21:23:02.857604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85a867a6bac3'
down_revision = '9633754af3cf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_task_goal_id_goal',
        source_table='task',
        referent_table='goal',
        local_cols=['goal_id'],
        remote_cols=['id']   # ВАЖНО: ссылка на goal.id
    )


def downgrade():
    op.drop_constraint('fk_task_goal_id_goal', 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')

    # ### end Alembic commands ###
