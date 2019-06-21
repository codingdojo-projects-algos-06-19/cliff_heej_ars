"""empty message

Revision ID: 560f794331ad
Revises: dcb9a7b553f9
Create Date: 2019-06-21 14:55:52.248651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '560f794331ad'
down_revision = 'dcb9a7b553f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pizzas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('method', sa.String(length=255), nullable=True),
    sa.Column('size', sa.String(length=255), nullable=True),
    sa.Column('crust', sa.String(length=255), nullable=True),
    sa.Column('toppings', sa.String(length=255), nullable=True),
    sa.Column('qty', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pizzas')
    # ### end Alembic commands ###
