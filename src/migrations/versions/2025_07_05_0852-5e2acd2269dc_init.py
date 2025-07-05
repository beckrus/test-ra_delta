"""init

Revision ID: 5e2acd2269dc
Revises:
Create Date: 2025-07-05 08:52:12.194758

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5e2acd2269dc"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "parcels",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("cost_usd", sa.Integer(), nullable=False),
        sa.Column("delivery_cost", sa.Float(), nullable=True),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("parcels")
    op.drop_table("types")
