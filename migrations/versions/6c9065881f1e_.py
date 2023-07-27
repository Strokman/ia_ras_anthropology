"""empty message

Revision ID: 6c9065881f1e
Revises: 655fa3138624
Create Date: 2023-07-27 10:52:15.625368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c9065881f1e'
down_revision = '655fa3138624'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('individs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('epoch_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'epochs', ['epoch_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('individs', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('epoch_id')

    # ### end Alembic commands ###
