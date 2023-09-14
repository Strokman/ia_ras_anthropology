"""empty message

Revision ID: 12870adafb60
Revises: bf4bbe8255f0
Create Date: 2023-09-14 12:59:54.900166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12870adafb60'
down_revision = 'bf4bbe8255f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.drop_column('path')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.add_column(sa.Column('path', sa.VARCHAR(length=128), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
