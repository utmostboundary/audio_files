"""init

Revision ID: 00001
Revises:
Create Date: 2025-03-29 12:13:48.750148

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "00001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_table(
        "audio_files",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_audio_files_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audio_files")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("audio_files")
    op.drop_table("users")
