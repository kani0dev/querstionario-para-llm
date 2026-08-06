"""add_is_active_to_users

Adiciona a coluna is_active (BOOLEAN) à tabela users.
- is_active: indica se o usuário está ativo (True) ou desativado (False)
- Default: TRUE para usuários existentes

Revision ID: cb9a1d4e2f5b
Revises: f60040853d77
Create Date: 2026-06-19 12:00:00.000000

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cb9a1d4e2f5b'
down_revision: str | Sequence[str] | None = 'f60040853d77'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE users
        ADD COLUMN is_active TINYINT(1) NOT NULL DEFAULT 1
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE users
        DROP COLUMN is_active
    """)
