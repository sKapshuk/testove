"""empty message

Revision ID: 283c04c4b384
Revises: 629b2d60d523
Create Date: 2023-08-16 21:40:37.224969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '283c04c4b384'
down_revision = '629b2d60d523'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=False))

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('date')

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_column('date')

    # ### end Alembic commands ###
