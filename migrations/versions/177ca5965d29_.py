"""empty message

Revision ID: 177ca5965d29
Revises: 
Create Date: 2020-05-23 19:10:07.826732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '177ca5965d29'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_started', sa.DateTime(), nullable=True),
    sa.Column('date_last_used', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
