"""initial_schema

Revision ID: 701a919f4025
Revises: 
Create Date: 2026-04-24 16:19:19.739900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '701a919f4025'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Users Table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('search_limit', sa.String(length=10), server_default='50'),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

    # 2. Medical Profiles Table (EAV)
    op.create_table(
        'user_health_profiles',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('illness_health_condition_diet_dislikes_name', sa.String(length=100), nullable=False, server_default='None'),
        sa.Column('illness_health_condition_diet_dislikes_value', sa.String(length=255), nullable=False, server_default='None'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # 3. Plates Table
    op.create_table(
        'plates',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('plate_name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # 4. Plate Items Table
    op.create_table(
        'plate_items',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('plate_id', sa.Integer(), nullable=False),
        sa.Column('product_code', sa.String(length=50), nullable=False),
        sa.Column('quantity_grams', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['plate_id'], ['plates.id'], ondelete='CASCADE')
    )


def downgrade() -> None:
    op.drop_table('plate_items')
    op.drop_table('plates')
    op.drop_table('user_health_profiles')
    op.drop_table('users')
