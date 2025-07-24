"""add protocols to asset interfaces

Revision ID: add_protocols_to_interfaces
Revises: b4fb73675c16
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_protocols_to_interfaces'
down_revision = 'b4fb73675c16'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Aggiungi il campo protocols alla tabella asset_interfaces
    op.add_column('asset_interfaces', sa.Column('protocols', postgresql.JSONB(), nullable=True, server_default='[]'))


def downgrade() -> None:
    # Rimuovi il campo protocols dalla tabella asset_interfaces
    op.drop_column('asset_interfaces', 'protocols') 