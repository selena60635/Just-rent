"""modify users table col phone

Revision ID: 43856ba4c792
Revises: b9f8b1ac7cc9
Create Date: 2024-04-30 00:39:14.033792

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '43856ba4c792'
down_revision = 'b9f8b1ac7cc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###