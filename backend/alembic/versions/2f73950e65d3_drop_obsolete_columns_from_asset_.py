"""drop_obsolete_columns_from_asset_communications

Revision ID: 2f73950e65d3
Revises: c3f55cb6de0f
Create Date: 2025-07-10 21:49:22.558133

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2f73950e65d3"
down_revision: Union[str, None] = "c3f55cb6de0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("asset_communications", "src_asset_id")
    op.drop_column("asset_communications", "dst_asset_id")
    op.drop_column("asset_communications", "protocol")
    op.drop_column("asset_communications", "port")
    op.drop_column("asset_communications", "frequency")
    op.drop_column("asset_communications", "description")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "asset_communications", sa.Column("src_asset_id", sa.UUID(), nullable=True)
    )
    op.add_column(
        "asset_communications", sa.Column("dst_asset_id", sa.UUID(), nullable=True)
    )
    op.add_column(
        "asset_communications", sa.Column("protocol", sa.String(50), nullable=True)
    )
    op.add_column(
        "asset_communications", sa.Column("port", sa.Integer(), nullable=True)
    )
    op.add_column(
        "asset_communications", sa.Column("frequency", sa.String(50), nullable=True)
    )
    op.add_column(
        "asset_communications", sa.Column("description", sa.Text(), nullable=True)
    )
