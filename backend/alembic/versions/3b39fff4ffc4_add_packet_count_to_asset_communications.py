"""add_packet_count_to_asset_communications

Revision ID: 3b39fff4ffc4
Revises: 347b6c409c3c
Create Date: 2025-07-10 21:45:09.351085

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3b39fff4ffc4"
down_revision: Union[str, None] = "347b6c409c3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aggiungi colonna packet_count a asset_communications
    op.add_column(
        "asset_communications",
        sa.Column("packet_count", sa.Integer(), nullable=True, default=0),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Rimuovi la colonna packet_count
    op.drop_column("asset_communications", "packet_count")
