"""empty message

Revision ID: 5ac86d3dbcb5
Revises: d0aed15c5318
Create Date: 2023-08-04 16:59:36.193926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ac86d3dbcb5'
down_revision = 'd0aed15c5318'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_column('image_id')

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=250),
               existing_nullable=True)
        batch_op.drop_column('image_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.alter_column('description',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
