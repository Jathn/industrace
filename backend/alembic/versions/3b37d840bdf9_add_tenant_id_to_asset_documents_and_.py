"""add_tenant_id_to_asset_documents_and_photos

Revision ID: 3b37d840bdf9
Revises: 4039a6e53359
Create Date: 2025-07-10 21:31:33.799043

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3b37d840bdf9"
down_revision: Union[str, None] = "4039a6e53359"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aggiungi colonna tenant_id a asset_documents
    op.add_column("asset_documents", sa.Column("tenant_id", sa.UUID(), nullable=True))

    # Aggiungi colonna tenant_id a asset_photos
    op.add_column("asset_photos", sa.Column("tenant_id", sa.UUID(), nullable=True))

    # Popola le colonne tenant_id con i tenant_id degli asset associati
    op.execute(
        """
        UPDATE asset_documents 
        SET tenant_id = assets.tenant_id 
        FROM assets 
        WHERE asset_documents.asset_id = assets.id
    """
    )

    op.execute(
        """
        UPDATE asset_photos 
        SET tenant_id = assets.tenant_id 
        FROM assets 
        WHERE asset_photos.asset_id = assets.id
    """
    )

    # Rendi le colonne NOT NULL dopo averle popolate
    op.alter_column("asset_documents", "tenant_id", nullable=False)
    op.alter_column("asset_photos", "tenant_id", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Rimuovi le colonne tenant_id
    op.drop_column("asset_documents", "tenant_id")
    op.drop_column("asset_photos", "tenant_id")
