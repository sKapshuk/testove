"""add date_edit + date_end

Revision ID: 629b2d60d523
Revises: e2a0454ba54c
Create Date: 2023-08-07 00:44:01.014234

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '629b2d60d523'
down_revision = 'e2a0454ba54c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_start', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('date_edit', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('date_end', sa.DateTime(), nullable=True))
        batch_op.drop_column('date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_column('date_end')
        batch_op.drop_column('date_edit')
        batch_op.drop_column('date_start')

    # ### end Alembic commands ###