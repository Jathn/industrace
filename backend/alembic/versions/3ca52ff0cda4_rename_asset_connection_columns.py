"""rename_asset_connection_columns

Revision ID: 3ca52ff0cda4
Revises: 3b37d840bdf9
Create Date: 2025-07-10 21:35:28.223703

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3ca52ff0cda4"
down_revision: Union[str, None] = "3b37d840bdf9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aggiungi colonna tenant_id a asset_connections
    op.add_column("asset_connections", sa.Column("tenant_id", sa.UUID(), nullable=True))

    # Aggiungi colonne mancanti a asset_connections
    op.add_column(
        "asset_connections", sa.Column("port_parent", sa.String(50), nullable=True)
    )
    op.add_column(
        "asset_connections", sa.Column("port_child", sa.String(50), nullable=True)
    )
    op.add_column(
        "asset_connections", sa.Column("protocol", sa.String(50), nullable=True)
    )
    op.add_column(
        "asset_connections", sa.Column("local_interface_id", sa.UUID(), nullable=True)
    )
    op.add_column(
        "asset_connections", sa.Column("remote_interface_id", sa.UUID(), nullable=True)
    )

    # Rinomina le colonne esistenti
    op.alter_column("asset_connections", "asset_id", new_column_name="parent_asset_id")
    op.alter_column(
        "asset_connections", "connected_asset_id", new_column_name="child_asset_id"
    )

    # Popola tenant_id con i tenant_id degli asset associati
    op.execute(
        """
        UPDATE asset_connections 
        SET tenant_id = assets.tenant_id 
        FROM assets 
        WHERE asset_connections.parent_asset_id = assets.id
    """
    )

    # Rendi tenant_id NOT NULL dopo averlo popolato
    op.alter_column("asset_connections", "tenant_id", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Rinomina le colonne di nuovo
    op.alter_column("asset_connections", "parent_asset_id", new_column_name="asset_id")
    op.alter_column(
        "asset_connections", "child_asset_id", new_column_name="connected_asset_id"
    )

    # Rimuovi le colonne aggiunte
    op.drop_column("asset_connections", "tenant_id")
    op.drop_column("asset_connections", "port_parent")
    op.drop_column("asset_connections", "port_child")
    op.drop_column("asset_connections", "protocol")
    op.drop_column("asset_connections", "local_interface_id")
    op.drop_column("asset_connections", "remote_interface_id")
