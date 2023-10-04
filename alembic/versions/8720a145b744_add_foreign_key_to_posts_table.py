"""add foreign-key to posts table

Revision ID: 8720a145b744
Revises: 371c4752dcb5
Create Date: 2023-09-28 05:24:20.201607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8720a145b744'
down_revision: Union[str, None] = '371c4752dcb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
