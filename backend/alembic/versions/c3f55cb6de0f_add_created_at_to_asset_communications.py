"""add_created_at_to_asset_communications

Revision ID: c3f55cb6de0f
Revises: 3b39fff4ffc4
Create Date: 2025-07-10 21:47:14.899781

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c3f55cb6de0f"
down_revision: Union[str, None] = "3b39fff4ffc4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "asset_communications", sa.Column("created_at", sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("asset_communications", "created_at")
