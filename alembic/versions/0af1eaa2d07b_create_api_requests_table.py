"""create_api_requests_table

Revision ID: 0af1eaa2d07b
Revises: 
Create Date: 2024-06-29 20:34:37.091679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0af1eaa2d07b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_type', sa.String(), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('response', sa.String(), nullable=False),
    sa.Column('status_code', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_requests')
    # ### end Alembic commands ###