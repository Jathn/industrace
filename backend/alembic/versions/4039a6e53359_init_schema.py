"""init schema

Revision ID: 4039a6e53359
Revises:
Create Date: 2025-06-13 14:42:28.554384

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4039a6e53359"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- TABELLE BASE ---
    op.create_table(
        "roles",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=50), unique=True, nullable=False),
        sa.Column("permissions", sa.JSON(), nullable=False, default=dict),
    )
    op.create_table(
        "tenants",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), unique=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("settings", sa.JSON(), default={}),
    )
    op.create_table(
        "sites",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("address", sa.Text()),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("parent_id", sa.UUID(), nullable=True),
    )
    op.create_table(
        "asset_types",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("icon", sa.String(length=50)),
        sa.Column("color", sa.String(length=7), default="#6366f1"),
        sa.Column("fields_schema", sa.dialects.postgresql.JSONB(), default=list),
        sa.Column("purdue_level", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "asset_statuses",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=True),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=200), nullable=True),
        sa.Column("color", sa.String(length=7), default="#64748b"),
        sa.Column("active", sa.Boolean(), default=True),
        sa.Column("order", sa.Integer(), default=0),
    )
    op.create_table(
        "manufacturers",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("description", sa.Text()),
        sa.Column("website", sa.String(length=255)),
        sa.Column("email", sa.String(length=255)),
        sa.Column("phone", sa.String(length=50)),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "locations",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("site_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), unique=True),
        sa.Column("description", sa.Text()),
        sa.Column("area", sa.String(length=255)),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(length=255), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_login", sa.DateTime()),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    )
    # ### CREAZIONE TABELLA ASSETS ###
    op.create_table(
        "assets",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("site_id", sa.UUID(), nullable=False),
        sa.Column("asset_type_id", sa.UUID(), nullable=False),
        sa.Column("status_id", sa.UUID(), nullable=False),
        sa.Column("location_id", sa.UUID(), nullable=True),
        sa.Column("manufacturer_id", sa.UUID(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("tag", sa.String(length=100)),
        sa.Column("serial_number", sa.String(length=100)),
        sa.Column("model", sa.String(length=100)),
        sa.Column("firmware_version", sa.String(length=50)),
        sa.Column("remote_access", sa.Boolean(), default=False),
        sa.Column("remote_access_type", sa.String(length=20), default="none"),
        sa.Column("last_update_date", sa.DateTime(), nullable=True),
        sa.Column("description", sa.Text()),
        sa.Column("custom_fields", sa.dialects.postgresql.JSONB(), default={}),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("last_seen", sa.DateTime()),
        sa.Column("map_x", sa.Float(), nullable=True),
        sa.Column("map_y", sa.Float(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("installation_date", sa.Date(), nullable=True),
        sa.Column("business_criticality", sa.String(), nullable=True),
        sa.Column("protocols", sa.dialects.postgresql.JSONB(), default=list),
        sa.Column("impact_value", sa.Integer(), default=1),
        sa.Column("physical_access_ease", sa.String(length=50), default="internal"),
        sa.Column("purdue_level", sa.Float(), default=0.0),
        sa.Column("exposure_level", sa.String(length=50), default="none"),
        sa.Column("update_status", sa.String(length=50), default="manual"),
        sa.Column("risk_score", sa.Float(), default=0.0),
        sa.Column("last_risk_assessment", sa.DateTime()),
    )
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "asset_documents",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("asset_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "asset_photos",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("asset_id", sa.UUID(), nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # --- TABELLE AGGIUNTIVE ---
    op.create_table(
        "api_keys",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("key_hash", sa.String(length=255), nullable=False, unique=True),
        sa.Column("scopes", sa.Text(), nullable=False, default="read"),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("expires_at", sa.DateTime()),
        sa.Column("last_used_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.UUID(), nullable=False),
        sa.Column(
            "rate_limit", sa.String(length=50), nullable=False, default="100/hour"
        ),
    )
    op.create_table(
        "suppliers",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("vat_number", sa.String(length=50)),
        sa.Column("tax_code", sa.String(length=50)),
        sa.Column("address", sa.String(length=255)),
        sa.Column("city", sa.String(length=100)),
        sa.Column("zip_code", sa.String(length=20)),
        sa.Column("province", sa.String(length=50)),
        sa.Column("country", sa.String(length=100)),
        sa.Column("phone", sa.String(length=50)),
        sa.Column("email", sa.String(length=255)),
        sa.Column("website", sa.String(length=255)),
        sa.Column("notes", sa.Text()),
        sa.Column("deleted_at", sa.DateTime()),
    )
    op.create_table(
        "supplier_documents",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("supplier_id", sa.UUID(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("filepath", sa.Text(), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "contacts",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("phone1", sa.String(length=50)),
        sa.Column("phone2", sa.String(length=50)),
        sa.Column("email", sa.String(length=255)),
        sa.Column("notes", sa.Text()),
        sa.Column("type", sa.String(length=50)),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime()),
    )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("entity", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.UUID()),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("ip_address", sa.String(length=45)),
        sa.Column("old_data", sa.JSON()),
        sa.Column("new_data", sa.JSON()),
        sa.Column("description", sa.String(length=255)),
    )
    op.create_table(
        "print_templates",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID()),
        sa.Column("key", sa.String(length=100), unique=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("name_translations", sa.dialects.postgresql.JSONB(), default=dict),
        sa.Column("description", sa.Text()),
        sa.Column(
            "description_translations", sa.dialects.postgresql.JSONB(), default=dict
        ),
        sa.Column("icon", sa.String(length=100)),
        sa.Column("component", sa.String(length=100)),
        sa.Column("options", sa.JSON(), default={}),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.create_table(
        "print_history",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("asset_id", sa.UUID(), nullable=False),
        sa.Column("template_id", sa.Integer(), nullable=False),
        sa.Column("generated_at", sa.DateTime(), nullable=True),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("file_size", sa.Integer()),
        sa.Column("generated_by", sa.UUID(), nullable=False),
    )
    op.create_table(
        "asset_connections",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("asset_id", sa.UUID(), nullable=False),
        sa.Column("connected_asset_id", sa.UUID(), nullable=False),
        sa.Column("connection_type", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "asset_interfaces",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("asset_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=50)),
        sa.Column("type", sa.String(length=50)),
        sa.Column("vlan", sa.String(length=50)),
        sa.Column("logical_port", sa.String(length=100)),
        sa.Column("physical_plug_label", sa.String(length=100)),
        sa.Column("details", sa.dialects.postgresql.JSONB()),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("ip_address", sa.String(length=50)),
        sa.Column("subnet_mask", sa.String(length=50)),
        sa.Column("default_gateway", sa.String(length=50)),
        sa.Column("mac_address", sa.String(length=50)),
        sa.Column("other", sa.String(length=255)),
    )
    op.create_table(
        "asset_communications",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("src_asset_id", sa.UUID(), nullable=False),
        sa.Column("dst_asset_id", sa.UUID(), nullable=False),
        sa.Column("protocol", sa.String(length=50), nullable=False),
        sa.Column("port", sa.Integer()),
        sa.Column("frequency", sa.String(length=50)),
        sa.Column("description", sa.Text()),
        sa.Column("src_interface_id", sa.UUID(), nullable=False),
        sa.Column("dst_interface_id", sa.UUID(), nullable=False),
    )
    op.create_table(
        "tenant_smtp_config",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("host", sa.String(length=255), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255)),
        sa.Column("password", sa.String(length=255)),
        sa.Column("from_email", sa.String(length=255), nullable=False),
        sa.Column("use_tls", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "location_floorplans",
        sa.Column("id", sa.UUID(), primary_key=True, nullable=False),
        sa.Column("tenant_id", sa.UUID(), nullable=False),
        sa.Column("location_id", sa.UUID(), nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "asset_contacts",
        sa.Column("asset_id", sa.UUID(), nullable=False),
        sa.Column("contact_id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("asset_id", "contact_id"),
    )
    op.create_table(
        "supplier_contacts",
        sa.Column("supplier_id", sa.UUID(), nullable=False),
        sa.Column("contact_id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("supplier_id", "contact_id"),
    )
    op.create_table(
        "site_contacts",
        sa.Column("site_id", sa.UUID(), nullable=False),
        sa.Column("contact_id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("site_id", "contact_id"),
    )
    op.create_table(
        "location_contacts",
        sa.Column("location_id", sa.UUID(), nullable=False),
        sa.Column("contact_id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("location_id", "contact_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("asset_photos")
    op.drop_table("asset_documents")
    # ### end Alembic commands ###
