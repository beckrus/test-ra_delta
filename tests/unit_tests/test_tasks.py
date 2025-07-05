from unittest.mock import AsyncMock, MagicMock, patch
from src.tasks.task_delivery_calc import calculate_delivery_cost_for_parcel


async def test_calculate_delivery_cost_for_parcel():
    with patch("src.tasks.task_delivery_calc.get_current_usd_rate", return_value=90.0):
        mock_parcels = [
            type("Parcel", (), {"id": 1, "weight": 1000, "cost_usd": 100, "delivery_cost": None})(),
            type("Parcel", (), {"id": 2, "weight": 500, "cost_usd": 50, "delivery_cost": None})(),
        ]
        mock_parcels_repo = AsyncMock()
        mock_parcels_repo.get_without_delivery_cost.return_value = mock_parcels
        mock_parcels_repo.update_delivery_cost_batch.return_value = 2

        mock_db = AsyncMock()
        mock_db.parcels = mock_parcels_repo
        mock_db.commit = AsyncMock()

        mock_ctx_manager = MagicMock()
        mock_ctx_manager.__aenter__.return_value = mock_db
        mock_ctx_manager.__aexit__.return_value = False

        with patch(
            "src.tasks.task_delivery_calc.get_db_manager_null_pull", return_value=mock_ctx_manager
        ):
            result = await calculate_delivery_cost_for_parcel()

            assert result is True
            mock_parcels_repo.get_without_delivery_cost.assert_awaited_once()
            mock_parcels_repo.update_delivery_cost_batch.assert_awaited_once()
            mock_db.commit.assert_awaited_once()
