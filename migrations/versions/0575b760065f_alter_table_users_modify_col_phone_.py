"""alter table users modify col phone VARCHAR(255)

Revision ID: 0575b760065f
Revises: 037f4097a245
Create Date: 2024-10-02 17:09:45.178144

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0575b760065f'
down_revision = '037f4097a245'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone',
               existing_type=sa.String(length=255),
               type_=mysql.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###