"""create_table_students

Cria a tabela students (herda de users via PK/FK)
- id: chave primária + estrangeira para users(id)
- student_uuid: UUID v7 único (VARCHAR(36) para compatibilidade com UUID7)

Revision ID: e4f3d58cc1ef
Revises: d0d428c1249f
Create Date: 2026-06-17 16:02:53.143760

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e4f3d58cc1ef'
down_revision: str | Sequence[str] | None = 'd0d428c1249f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE students (
            id INT PRIMARY KEY,
            student_uuid VARCHAR(36) NOT NULL UNIQUE,
            FOREIGN KEY (id) REFERENCES users(id)
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS students")
