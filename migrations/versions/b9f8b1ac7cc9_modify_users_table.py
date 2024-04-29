"""modify users table

Revision ID: b9f8b1ac7cc9
Revises: 2eff7a36d0fd
Create Date: 2024-04-28 20:07:27.080787

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b9f8b1ac7cc9'
down_revision = '2eff7a36d0fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('role', sa.String(length=255), nullable=False))
        batch_op.alter_column('phone',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', mysql.VARCHAR(length=255), nullable=False))
        batch_op.alter_column('phone',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.drop_column('role')
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
