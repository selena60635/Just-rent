"""creat booking table

Revision ID: 7835a5bebe56
Revises: 5686ef577ae2
Create Date: 2024-04-24 00:00:10.774848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7835a5bebe56'
down_revision = '5686ef577ae2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.Column('rent_location_id', sa.Integer(), nullable=True),
    sa.Column('return_location_id', sa.Integer(), nullable=True),
    sa.Column('pickup_date', sa.DateTime(), nullable=True),
    sa.Column('return_date', sa.DateTime(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ),
    sa.ForeignKeyConstraint(['rent_location_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['return_location_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_booking_pickup_date'), ['pickup_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_booking_return_date'), ['return_date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_booking_return_date'))
        batch_op.drop_index(batch_op.f('ix_booking_pickup_date'))

    op.drop_table('booking')
    # ### end Alembic commands ###
