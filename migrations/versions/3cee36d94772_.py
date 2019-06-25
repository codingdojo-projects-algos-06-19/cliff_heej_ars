"""empty message

Revision ID: 3cee36d94772
Revises: cb221a19f672
Create Date: 2019-06-25 15:55:52.356105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cee36d94772'
down_revision = 'cb221a19f672'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addresses', sa.Column('zip_code', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('addresses', 'zip_code')
    # ### end Alembic commands ###
