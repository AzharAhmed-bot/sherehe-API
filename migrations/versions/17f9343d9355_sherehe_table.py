"""sherehe table

Revision ID: 17f9343d9355
Revises: 3e68ee8ac9cc
Create Date: 2024-01-25 14:38:13.813057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17f9343d9355'
down_revision = '3e68ee8ac9cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sherehe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('paid', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('paid')
        batch_op.drop_column('password')
        batch_op.drop_column('amount')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('password', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('paid', sa.BOOLEAN(), nullable=True))

    op.drop_table('sherehe')
    # ### end Alembic commands ###
