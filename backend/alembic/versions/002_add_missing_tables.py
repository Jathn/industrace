"""add missing tables

Revision ID: 002
Revises: 001
Create Date: 2025-07-24 13:35:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Create audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('entity', sa.String(length=100), nullable=False),
        sa.Column('entity_id', sa.UUID(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('old_data', sa.JSON(), nullable=True),
        sa.Column('new_data', sa.JSON(), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create api_keys table
    op.create_table('api_keys',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('key_hash', sa.String(length=255), nullable=False),
        sa.Column('scopes', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.UUID(), nullable=False),
        sa.Column('rate_limit', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key_hash')
    )

    # Create asset_interfaces table
    op.create_table('asset_interfaces',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('subnet_mask', sa.String(length=50), nullable=True),
        sa.Column('mac_address', sa.String(length=50), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=True),
        sa.Column('vlan', sa.String(length=50), nullable=True),
        sa.Column('logical_port', sa.String(length=50), nullable=True),
        sa.Column('physical_plug_label', sa.String(length=50), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('default_gateway', sa.String(length=50), nullable=True),
        sa.Column('other', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create asset_connections table
    op.create_table('asset_connections',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('parent_asset_id', sa.UUID(), nullable=True),
        sa.Column('child_asset_id', sa.UUID(), nullable=True),
        sa.Column('connection_type', sa.String(length=50), nullable=False),
        sa.Column('port_parent', sa.String(length=50), nullable=True),
        sa.Column('port_child', sa.String(length=50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('local_interface_id', sa.UUID(), nullable=True),
        sa.Column('remote_interface_id', sa.UUID(), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['child_asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['local_interface_id'], ['asset_interfaces.id'], ),
        sa.ForeignKeyConstraint(['parent_asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['remote_interface_id'], ['asset_interfaces.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create asset_communications table
    op.create_table('asset_communications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('src_interface_id', sa.UUID(), nullable=True),
        sa.Column('dst_interface_id', sa.UUID(), nullable=True),
        sa.Column('site_id', sa.UUID(), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['dst_interface_id'], ['asset_interfaces.id'], ),
        sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ),
        sa.ForeignKeyConstraint(['src_interface_id'], ['asset_interfaces.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create asset_documents table
    op.create_table('asset_documents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create asset_photos table
    op.create_table('asset_photos',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create print_templates table
    op.create_table('print_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('key', sa.String(length=100), nullable=False),
        sa.Column('name_translations', sa.JSON(), nullable=True),
        sa.Column('description_translations', sa.JSON(), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('component', sa.String(length=100), nullable=True),
        sa.Column('options', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create print_history table
    op.create_table('print_history',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('generated_at', sa.DateTime(), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('generated_by', sa.UUID(), nullable=False),
        sa.Column('options', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['generated_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['template_id'], ['print_templates.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create tenant_smtp_config table
    op.create_table('tenant_smtp_config',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('host', sa.String(), nullable=False),
        sa.Column('port', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('from_email', sa.String(), nullable=False),
        sa.Column('use_tls', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id')
    )

    # Create relationship tables
    op.create_table('site_contacts',
        sa.Column('site_id', sa.UUID(), nullable=False),
        sa.Column('contact_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('site_id', 'contact_id')
    )

    op.create_table('supplier_contacts',
        sa.Column('supplier_id', sa.UUID(), nullable=False),
        sa.Column('contact_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('supplier_id', 'contact_id')
    )

    op.create_table('asset_contacts',
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('contact_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('asset_id', 'contact_id')
    )

    # Create indexes
    op.create_index('ix_audit_logs_tenant_id', 'audit_logs', ['tenant_id'])
    op.create_index('ix_api_keys_tenant_id', 'api_keys', ['tenant_id'])
    op.create_index('ix_print_templates_tenant_id', 'print_templates', ['tenant_id'])
    op.create_index('ix_print_templates_key', 'print_templates', ['key'])


def downgrade():
    op.drop_index('ix_print_templates_key', table_name='print_templates')
    op.drop_index('ix_print_templates_tenant_id', table_name='print_templates')
    op.drop_index('ix_api_keys_tenant_id', table_name='api_keys')
    op.drop_index('ix_audit_logs_tenant_id', table_name='audit_logs')
    op.drop_table('asset_contacts')
    op.drop_table('supplier_contacts')
    op.drop_table('site_contacts')
    op.drop_table('tenant_smtp_config')
    op.drop_table('print_history')
    op.drop_table('print_templates')
    op.drop_table('asset_photos')
    op.drop_table('asset_documents')
    op.drop_table('asset_communications')
    op.drop_table('asset_connections')
    op.drop_table('asset_interfaces')
    op.drop_table('api_keys')
    op.drop_table('audit_logs') 