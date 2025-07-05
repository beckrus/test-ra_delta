import pytest
from src.tasks.task_delivery_calc import calc_cost


@pytest.mark.parametrize(
    "weight, cost_usd, usd_rate, result",
    [
        (170, 544, 78.8354, 435.57),
        (1, 50, 78.8354, 39.46),
        (200, 350, 78.8354, 283.81),
        (10000, 30, 78.8354, 417.83),
    ],
)
def test_calc_cost(weight: float, cost_usd: float, usd_rate: float, result: float):
    assert calc_cost(weight, cost_usd, usd_rate) == result
