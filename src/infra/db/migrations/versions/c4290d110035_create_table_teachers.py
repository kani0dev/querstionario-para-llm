"""create_table_teachers

Cria a tabela teachers (herda de users via PK/FK)
- id: chave primária + estrangeira para users(id)
- teacher_uuid: UUID v7 único

Revision ID: c4290d110035
Revises: e4f3d58cc1ef
Create Date: 2026-06-17 16:03:28.706422

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c4290d110035'
down_revision: str | Sequence[str] | None = 'e4f3d58cc1ef'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE teachers (
            id INT PRIMARY KEY,
            teacher_uuid VARCHAR(36) NOT NULL UNIQUE,
            FOREIGN KEY (id) REFERENCES users(id)
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS teachers")
