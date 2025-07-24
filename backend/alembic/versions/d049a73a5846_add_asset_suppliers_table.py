"""add_asset_suppliers_table

Revision ID: d049a73a5846
Revises: 3ca52ff0cda4
Create Date: 2025-07-10 21:36:57.351829

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d049a73a5846"
down_revision: Union[str, None] = "3ca52ff0cda4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Crea la tabella asset_suppliers
    op.create_table(
        "asset_suppliers",
        sa.Column("asset_id", sa.UUID(), nullable=False),
        sa.Column("supplier_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["supplier_id"], ["suppliers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("asset_id", "supplier_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Rimuovi la tabella asset_suppliers
    op.drop_table("asset_suppliers")
