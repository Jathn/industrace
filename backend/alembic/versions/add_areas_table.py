"""add areas table

Revision ID: add_areas_table
Revises: add_protocols_to_interfaces
Create Date: 2024-07-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_areas_table'
down_revision = 'add_protocols_to_interfaces'
branch_labels = None
depends_on = None


def upgrade():
    # Create areas table
    op.create_table('areas',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('site_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('typology', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add area_id column to locations table
    op.add_column('locations', sa.Column('area_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'locations', 'areas', ['area_id'], ['id'])
    
    # Add area_id column to assets table
    op.add_column('assets', sa.Column('area_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'assets', 'areas', ['area_id'], ['id'])
    
    # Drop the old area column from locations table
    op.drop_column('locations', 'area')


def downgrade():
    # Add back the old area column to locations table
    op.add_column('locations', sa.Column('area', sa.String(length=255), nullable=True))
    
    # Drop foreign key constraints
    op.drop_constraint(None, 'assets', type_='foreignkey')
    op.drop_constraint(None, 'locations', type_='foreignkey')
    
    # Drop area_id columns
    op.drop_column('assets', 'area_id')
    op.drop_column('locations', 'area_id')
    
    # Drop areas table
    op.drop_table('areas') 