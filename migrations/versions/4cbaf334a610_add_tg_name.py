"""Add tg name

Revision ID: 4cbaf334a610
Revises: 621b88211409
Create Date: 2024-06-12 11:56:12.663208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cbaf334a610'
down_revision: Union[str, None] = '621b88211409'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('tg_username', sa.String(length=255), nullable=True))
    op.create_unique_constraint(None, 'users', ['tg_username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'tg_username')
    # ### end Alembic commands ###