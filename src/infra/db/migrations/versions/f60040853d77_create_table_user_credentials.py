"""create_table_user_credentials

Cria a tabela user_credentials para armazenar senhas hasheadas (Argon2)
- user_id: PK + FK para users(id) com ON DELETE CASCADE
- password: hash Argon2
- last_password_change: data da última alteração
- fail_attempts: contagem de tentativas falhas

Revision ID: f60040853d77
Revises: c4290d110035
Create Date: 2026-06-17 16:04:22.796724

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f60040853d77'
down_revision: str | Sequence[str] | None = 'c4290d110035'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE user_credentials (
            user_id INT NOT NULL,
            password VARCHAR(255) NOT NULL,
            last_password_change DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fail_attempts INT NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id),
            CONSTRAINT fk_user_credentials_user
                FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS user_credentials")
