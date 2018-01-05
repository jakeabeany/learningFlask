"""added caption fields

Revision ID: 97bddcde272c
Revises: c8f90285e350
Create Date: 2018-01-05 17:30:23.777213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97bddcde272c'
down_revision = 'c8f90285e350'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photo', sa.Column('main_caption', sa.String(length=200), nullable=True))
    op.add_column('photo', sa.Column('sub_caption', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photo', 'sub_caption')
    op.drop_column('photo', 'main_caption')
    # ### end Alembic commands ###