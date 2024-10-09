"""creat tables users,cars,booking,location,likes,level_price

Revision ID: 10401204ddc9
Revises: 
Create Date: 2024-10-07 03:26:11.671415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10401204ddc9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('level_price',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('special_price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('latitude', sa.DECIMAL(precision=18, scale=15), nullable=True),
    sa.Column('longitude', sa.DECIMAL(precision=18, scale=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=255), nullable=False),
    sa.Column('language', sa.String(length=255), nullable=False),
    sa.Column('hour_format', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('displacement', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=255), nullable=False),
    sa.Column('seat', sa.Integer(), nullable=False),
    sa.Column('door', sa.Integer(), nullable=False),
    sa.Column('car_length', sa.Integer(), nullable=False),
    sa.Column('wheelbase', sa.Integer(), nullable=False),
    sa.Column('power_type', sa.String(length=255), nullable=False),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('model', sa.String(length=255), nullable=True),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['price'], ['level_price.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('pickup_date', sa.Date(), nullable=False),
    sa.Column('return_date', sa.Date(), nullable=False),
    sa.Column('pickup_time', sa.Time(), nullable=False),
    sa.Column('return_time', sa.Time(), nullable=False),
    sa.Column('pick_up_loc', sa.Integer(), nullable=False),
    sa.Column('drop_off_loc', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ),
    sa.ForeignKeyConstraint(['drop_off_loc'], ['location.id'], ),
    sa.ForeignKeyConstraint(['pick_up_loc'], ['location.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_booking_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_booking_pickup_time'), ['pickup_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_booking_return_time'), ['return_time'], unique=False)

    op.create_table('likes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'car_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_booking_return_time'))
        batch_op.drop_index(batch_op.f('ix_booking_pickup_time'))
        batch_op.drop_index(batch_op.f('ix_booking_created_at'))

    op.drop_table('booking')
    op.drop_table('cars')
    op.drop_table('users')
    op.drop_table('location')
    op.drop_table('level_price')
    # ### end Alembic commands ###
