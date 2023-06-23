"""empty message

Revision ID: ba981ea4ec14
Revises: 41fcdc202626
Create Date: 2023-06-23 15:15:54.735391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba981ea4ec14'
down_revision = '41fcdc202626'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('researchers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('affiliation', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('researchers', schema=None) as batch_op:
        batch_op.drop_column('affiliation')

    # ### end Alembic commands ###
