"""add_tenant_and_site_to_asset_communications

Revision ID: 347b6c409c3c
Revises: d049a73a5846
Create Date: 2025-07-10 21:39:15.536797

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "347b6c409c3c"
down_revision: Union[str, None] = "d049a73a5846"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aggiungi colonne mancanti a asset_communications
    op.add_column(
        "asset_communications", sa.Column("tenant_id", sa.UUID(), nullable=True)
    )
    op.add_column(
        "asset_communications", sa.Column("site_id", sa.UUID(), nullable=True)
    )

    # Popola le colonne con i valori degli asset associati
    op.execute(
        """
        UPDATE asset_communications 
        SET tenant_id = assets.tenant_id, site_id = assets.site_id
        FROM assets, asset_interfaces
        WHERE asset_communications.src_interface_id = asset_interfaces.id 
        AND asset_interfaces.asset_id = assets.id
    """
    )

    # Rendi le colonne NOT NULL dopo averle popolate
    op.alter_column("asset_communications", "tenant_id", nullable=False)
    op.alter_column("asset_communications", "site_id", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Rimuovi le colonne aggiunte
    op.drop_column("asset_communications", "tenant_id")
    op.drop_column("asset_communications", "site_id")
