"""empty message

Revision ID: b7020b277bb8
Revises: 48edf8c45b74
Create Date: 2023-12-01 09:31:49.637766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7020b277bb8'
down_revision = '48edf8c45b74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('individs', schema=None) as batch_op:
        batch_op.drop_column('is_deleted')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('individs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
