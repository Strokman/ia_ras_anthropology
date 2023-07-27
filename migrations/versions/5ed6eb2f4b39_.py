"""empty message

Revision ID: 5ed6eb2f4b39
Revises: 049684381d5c
Create Date: 2023-07-10 07:59:42.016206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ed6eb2f4b39'
down_revision = '049684381d5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('graves', schema=None) as batch_op:
        batch_op.add_column(sa.Column('individ_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'individs', ['individ_id'], ['id'])

    with op.batch_alter_table('individs', schema=None) as batch_op:
        batch_op.drop_constraint('individs_grave_id_fkey', type_='foreignkey')
        batch_op.drop_column('grave_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('individs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('grave_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('individs_grave_id_fkey', 'graves', ['grave_id'], ['id'])

    with op.batch_alter_table('graves', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('individ_id')

    # ### end Alembic commands ###