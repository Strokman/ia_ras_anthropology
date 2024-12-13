"""rename comment_temp to comment

Revision ID: 7205ddd23abb
Revises: f5432ece63e0
Create Date: 2024-12-13 17:06:26.294976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7205ddd23abb'
down_revision = 'f5432ece63e0'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'individs',  # Имя таблицы
        'comment_temp',  # Текущее имя колонки
        new_column_name='comment'  # Новое имя колонки
    )



def downgrade():
    op.alter_column(
        'individs',  # Имя таблицы
        'comment',  # Текущее имя колонки
        new_column_name='comment_temp'  # Новое имя колонки
    )
