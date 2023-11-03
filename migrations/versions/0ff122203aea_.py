"""empty message

Revision ID: 0ff122203aea
Revises: 
Create Date: 2023-11-03 13:29:56.081637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ff122203aea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('graves', schema=None) as batch_op:
        batch_op.alter_column('tachymeter_point',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('graves', schema=None) as batch_op:
        batch_op.alter_column('tachymeter_point',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=32),
               existing_nullable=True)

    # ### end Alembic commands ###
