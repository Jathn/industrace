"""add_status_column_to_print_history

Revision ID: e01ebd2a1fa7
Revises: 2f73950e65d3
Create Date: 2025-07-10 21:57:11.332219

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e01ebd2a1fa7"
down_revision: Union[str, None] = "2f73950e65d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aggiungi solo la colonna status alla tabella print_history
    op.add_column(
        "print_history",
        sa.Column(
            "status", sa.String(length=50), nullable=True, server_default="completed"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Rimuovi la colonna status dalla tabella print_history
    op.drop_column("print_history", "status")
