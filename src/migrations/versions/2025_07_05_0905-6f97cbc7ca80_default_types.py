"""default types

Revision ID: 6f97cbc7ca80
Revises: 5e2acd2269dc
Create Date: 2025-07-05 09:05:54.454454

"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = "6f97cbc7ca80"
down_revision: Union[str, Sequence[str], None] = "5e2acd2269dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    
    result = connection.execute(text("SELECT COUNT(*) FROM types")).scalar()
    
    if result == 0:
        default_types = [
            "('одежда')",
            "('электроника')",
            "('разное')"
        ]
        
        values = ", ".join(default_types)
        connection.execute(
            text(f"INSERT INTO types (name) VALUES {values}")
        )
        print("Added default parcel types: одежда, электроника, разное")
    else:
        print("Types table already contains data, skipping initialization")


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()
    connection.execute(
        text("DELETE FROM types WHERE name IN ('одежда', 'электроника', 'разное')")
    )
