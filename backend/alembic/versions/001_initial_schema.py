"""initial schema

Revision ID: 001
Revises: 
Create Date: 2025-07-24 13:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tenants table first
    op.create_table('tenants',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # Create roles table
    op.create_table('roles',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('permissions', sa.JSON(), nullable=True),
        sa.Column('is_inheritable', sa.Boolean(), nullable=True),
        sa.Column('parent_role_id', sa.UUID(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['parent_role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create users table
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('role_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create sites table
    op.create_table('sites',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('contact_email', sa.String(length=255), nullable=True),
        sa.Column('contact_phone', sa.String(length=50), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('parent_id', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['sites.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create areas table
    op.create_table('areas',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('site_id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('typology', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create suppliers table
    op.create_table('suppliers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('zip_code', sa.String(length=20), nullable=True),
        sa.Column('province', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('vat_number', sa.String(length=50), nullable=True),
        sa.Column('tax_code', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create manufacturers table
    op.create_table('manufacturers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create contacts table
    op.create_table('contacts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('role', sa.String(length=100), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('phone1', sa.String(length=50), nullable=True),
        sa.Column('phone2', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('type', sa.String(length=50), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create asset_types table
    op.create_table('asset_types',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=20), nullable=True),
        sa.Column('fields_schema', sa.JSON(), nullable=True),
        sa.Column('purdue_level', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create asset_statuses table
    op.create_table('asset_statuses',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create assets table
    op.create_table('assets',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('serial_number', sa.String(length=100), nullable=True),
        sa.Column('model', sa.String(length=100), nullable=True),
        sa.Column('manufacturer_name', sa.String(length=255), nullable=True),
        sa.Column('firmware_version', sa.String(length=50), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('mac_address', sa.String(length=50), nullable=True),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('site_id', sa.UUID(), nullable=False),
        sa.Column('area_id', sa.UUID(), nullable=True),
        sa.Column('asset_type_id', sa.UUID(), nullable=False),
        sa.Column('supplier_id', sa.UUID(), nullable=True),
        sa.Column('status_id', sa.UUID(), nullable=True),
        sa.Column('tag', sa.String(length=100), nullable=True),
        sa.Column('remote_access', sa.Boolean(), nullable=True),
        sa.Column('remote_access_type', sa.String(length=50), nullable=True),
        sa.Column('last_update_date', sa.DateTime(), nullable=True),
        sa.Column('custom_fields', sa.JSON(), nullable=True),
        sa.Column('map_x', sa.Float(), nullable=True),
        sa.Column('map_y', sa.Float(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('installation_date', sa.DateTime(), nullable=True),
        sa.Column('business_criticality', sa.String(length=50), nullable=True),
        sa.Column('protocols', sa.JSON(), nullable=True),
        sa.Column('impact_value', sa.String(length=20), nullable=True),
        sa.Column('physical_access_ease', sa.String(length=20), nullable=True),
        sa.Column('purdue_level', sa.String(length=20), nullable=True),
        sa.Column('exposure_level', sa.String(length=20), nullable=True),
        sa.Column('update_status', sa.String(length=50), nullable=True),
        sa.Column('last_risk_assessment', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['area_id'], ['areas.id'], ),
        sa.ForeignKeyConstraint(['asset_type_id'], ['asset_types.id'], ),
        sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['asset_statuses.id'], ),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('assets')
    op.drop_table('asset_statuses')
    op.drop_table('asset_types')
    op.drop_table('contacts')
    op.drop_table('manufacturers')
    op.drop_table('suppliers')
    op.drop_table('areas')
    op.drop_table('sites')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('tenants') 