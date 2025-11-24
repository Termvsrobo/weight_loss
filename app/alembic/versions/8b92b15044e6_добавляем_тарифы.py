"""Добавляем тарифы

Revision ID: 8b92b15044e6
Revises: b2f3e6632c70
Create Date: 2025-10-30 17:51:23.252805

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8b92b15044e6"
down_revision: Union[str, Sequence[str], None] = "b2f3e6632c70"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    meta = sa.MetaData()
    meta.reflect(bind=op.get_bind(), only=("tariffs",))
    table = sa.Table("tariffs", meta)
    op.bulk_insert(
        table,
        [
            dict(
                name="Стартовый", percent=1, description="Стартовый тариф для новичков"
            ),
            dict(name="Профи", percent=3, description="Описание профи тарифа"),
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("truncate tariffs")
