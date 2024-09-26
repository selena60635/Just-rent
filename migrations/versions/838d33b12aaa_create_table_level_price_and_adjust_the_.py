"""create table level_price, and adjust the related cols in booking and cars.

Revision ID: 838d33b12aaa
Revises: 03b48966c6c1
Create Date: 2024-09-24 16:07:10.280828

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '838d33b12aaa'
down_revision = '03b48966c6c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'level_price', ['price'], ['id'])
        batch_op.drop_column('available_time')
        batch_op.drop_column('is_available')
        batch_op.drop_column('location_id')
        batch_op.drop_column('last_return_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_return_time', mysql.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('location_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('is_available', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('available_time', mysql.DATETIME(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
