"""empty message

Revision ID: 8075bfdea493
Revises: 
Create Date: 2022-06-21 13:58:23.396230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8075bfdea493'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userinfo')
    # ### end Alembic commands ###
