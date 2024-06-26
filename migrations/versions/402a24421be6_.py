"""empty message

Revision ID: 402a24421be6
Revises: 36c6fb969595
Create Date: 2024-05-05 11:42:29.932670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '402a24421be6'
down_revision = '36c6fb969595'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('federal_districts')
    with op.batch_alter_table('regions', schema=None) as batch_op:
        batch_op.drop_constraint('regions_federal_districts_id_fkey', type_='foreignkey')
        batch_op.drop_column('federal_districts_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('regions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('federal_districts_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('regions_federal_districts_id_fkey', 'federal_districts', ['federal_districts_id'], ['id'])

    op.create_table('federal_districts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='federal_districts_pkey')
    )
    # ### end Alembic commands ###
