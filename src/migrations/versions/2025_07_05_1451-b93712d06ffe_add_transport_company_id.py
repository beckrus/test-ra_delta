"""add transport_company_id

Revision ID: b93712d06ffe
Revises: 6f97cbc7ca80
Create Date: 2025-07-05 14:51:26.598350

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b93712d06ffe"
down_revision: Union[str, Sequence[str], None] = "6f97cbc7ca80"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("parcels", sa.Column("transport_company_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("parcels", "transport_company_id")
