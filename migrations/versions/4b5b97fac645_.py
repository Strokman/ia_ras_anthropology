"""empty message

Revision ID: 4b5b97fac645
Revises: 6ba51b15dd14
Create Date: 2023-08-02 22:25:03.109392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b5b97fac645'
down_revision = '6ba51b15dd14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sites_researchers',
    sa.Column('archaeological_site_id', sa.Integer(), nullable=True),
    sa.Column('researcher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['archaeological_site_id'], ['archaeological_sites.id'], ),
    sa.ForeignKeyConstraint(['researcher_id'], ['researchers.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sites_researchers')
    # ### end Alembic commands ###
