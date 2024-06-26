"""stock table add stock_id

Revision ID: 6e7f546e3033
Revises: b65601956f85
Create Date: 2024-04-30 12:51:06.720986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel                                 # New


# revision identifiers, used by Alembic.
revision: str = '6e7f546e3033'
down_revision: Union[str, None] = 'b65601956f85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stocks', sa.Column('stock_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_index(op.f('ix_stocks_stock_id'), 'stocks', ['stock_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_stocks_stock_id'), table_name='stocks')
    op.drop_column('stocks', 'stock_id')
    # ### end Alembic commands ###
