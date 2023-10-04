"""add last few columns

Revision ID: 7d28af25a295
Revises: 8720a145b744
Create Date: 2023-09-28 09:25:51.903957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d28af25a295'
down_revision: Union[str, None] = '8720a145b744'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                    nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','title')
    op.drop_column('posts','content')
    op.drop_column('posts','published')
    op.drop_column('post','created_at')
    pass
