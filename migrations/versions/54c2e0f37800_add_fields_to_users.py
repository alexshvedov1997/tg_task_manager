"""Add fields to Users

Revision ID: 54c2e0f37800
Revises: 37fd8c6f9bbd
Create Date: 2024-06-09 06:40:59.753064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54c2e0f37800'
down_revision: Union[str, None] = '37fd8c6f9bbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=255), nullable=True))
    op.drop_constraint('users_chat_id_key', 'users', type_='unique')
    op.drop_column('users', 'chat_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('chat_id', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.create_unique_constraint('users_chat_id_key', 'users', ['chat_id'])
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###
