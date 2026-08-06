"""add_users_jadir_claudia

Adiciona dois usuários iniciais:
- jadir (student) com senha '123'
- claudia (teacher) com senha '123'

Revision ID: b3a7c9d2e1f0
Revises: abc123def456
Create Date: 2026-07-16 12:00:00.000000

"""
from collections.abc import Sequence

import uuid_utils as uuid
from alembic import op
from argon2 import PasswordHasher

# revision identifiers, used by Alembic.
revision: str = 'b3a7c9d2e1f0'
down_revision: str | Sequence[str] | None = 'abc123def456'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ph = PasswordHasher()


def upgrade() -> None:
    student_uuid = str(uuid.uuid7())
    teacher_uuid = str(uuid.uuid7())
    hashed_password = ph.hash("123")

    op.execute("""
        INSERT INTO users (name, role, is_active, create_at)
        VALUES ('jadir', 'STUDENT', 1, NOW())
    """)
    op.execute("SET @student_id = LAST_INSERT_ID()")

    op.execute("""
        INSERT INTO users (name, role, is_active, create_at)
        VALUES ('claudia', 'TEACHER', 1, NOW())
    """)
    op.execute("SET @teacher_id = LAST_INSERT_ID()")

    op.execute(f"""
        INSERT INTO students (id, student_uuid)
        VALUES (@student_id, '{student_uuid}')
    """)

    op.execute(f"""
        INSERT INTO teachers (id, teacher_uuid)
        VALUES (@teacher_id, '{teacher_uuid}')
    """)

    op.execute(f"""
        INSERT INTO user_credentials (user_id, password, last_password_change, fail_attempts)
        VALUES (@student_id, '{hashed_password}', NOW(), 0)
    """)

    op.execute(f"""
        INSERT INTO user_credentials (user_id, password, last_password_change, fail_attempts)
        VALUES (@teacher_id, '{hashed_password}', NOW(), 0)
    """)


def downgrade() -> None:
    op.execute("""
        DELETE uc FROM user_credentials uc
        JOIN users u ON uc.user_id = u.id
        WHERE u.name IN ('jadir', 'claudia')
    """)
    op.execute("""
        DELETE s FROM students s
        JOIN users u ON s.id = u.id
        WHERE u.name = 'jadir'
    """)
    op.execute("""
        DELETE t FROM teachers t
        JOIN users u ON t.id = u.id
        WHERE u.name = 'claudia'
    """)
    op.execute("""
        DELETE FROM users WHERE name IN ('jadir', 'claudia')
    """)
