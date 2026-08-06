"""change_role_enum_to_varchar

Altera a coluna role de ENUM('STUDENT','TEACHER') para VARCHAR(20)
para permitir valores inseridos manualmente como 'admin'.

Revision ID: abc123def456
Revises: cb9a1d4e2f5b
Create Date: 2026-07-07 10:00:00.000000

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'abc123def456'
down_revision: str | Sequence[str] | None = 'cb9a1d4e2f5b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE users
        MODIFY COLUMN role VARCHAR(20) NOT NULL DEFAULT 'STUDENT'
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE users
        MODIFY COLUMN role ENUM('STUDENT', 'TEACHER') NOT NULL DEFAULT 'STUDENT'
    """)
