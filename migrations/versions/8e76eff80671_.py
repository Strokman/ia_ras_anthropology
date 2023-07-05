"""empty message

Revision ID: 8e76eff80671
Revises: d7c5bc7c5f85
Create Date: 2023-07-05 12:32:01.523277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e76eff80671'
down_revision = 'd7c5bc7c5f85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('researchers', schema=None) as batch_op:
        batch_op.alter_column('affiliation',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('researchers', schema=None) as batch_op:
        batch_op.alter_column('affiliation',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)

    # ### end Alembic commands ###