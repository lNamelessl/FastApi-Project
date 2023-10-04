"""add user table'

Revision ID: 371c4752dcb5
Revises: 9a4e7c894a36
Create Date: 2023-09-27 09:00:09.313869

"""
from cgitb import text
import email
from time import timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '371c4752dcb5'
down_revision: Union[str, None] = '9a4e7c894a36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False,),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                    server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
