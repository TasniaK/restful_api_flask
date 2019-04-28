"""empty message

Revision ID: 2cb7ebe46e8b
Revises: 
Create Date: 2019-04-28 20:50:24.901463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cb7ebe46e8b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('done', sa.Boolean(create_constraint=False), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_description'), 'task', ['description'], unique=True)
    op.create_index(op.f('ix_task_done'), 'task', ['done'], unique=False)
    op.create_index(op.f('ix_task_title'), 'task', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_title'), table_name='task')
    op.drop_index(op.f('ix_task_done'), table_name='task')
    op.drop_index(op.f('ix_task_description'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###