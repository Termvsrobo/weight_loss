"""Добавляем стартовый тариф всем пользователям

Revision ID: d1626166e1ea
Revises: 8b92b15044e6
Create Date: 2025-10-30 18:54:39.870951

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d1626166e1ea"
down_revision: Union[str, Sequence[str], None] = "8b92b15044e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "update users set tariff_id = (select id from tariffs where name = 'Стартовый') where tariff_id is null"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("update users set tariff_id=null")
