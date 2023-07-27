"""empty message

Revision ID: 041d28f452a9
Revises: 6905570c2371
Create Date: 2023-07-06 17:24:03.030951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '041d28f452a9'
down_revision = '6905570c2371'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('archaeological_sites', schema=None) as batch_op:
        batch_op.drop_constraint('archaeological_sites_researcher_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'researchers', ['researcher_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('archaeological_sites', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('archaeological_sites_researcher_id_fkey', 'researchers', ['researcher_id'], ['id'])

    # ### end Alembic commands ###