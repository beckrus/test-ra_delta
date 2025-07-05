import logging
import math
from src.api.dependencies import get_db_manager_null_pull
from src.utils.exchange_rate import get_current_usd_rate
from src.schemas.parcels import ParcelUpdateCostDTO
from src.tasks.taskiq import broker

logger = logging.getLogger(__name__)


def calc_cost(weight: float, cost_usd: float, usd_rate: float):
    """ weight in gramms
        Стоимость = (вес в кг * 0.5 + стоимость содержимого в долларах * 0.01 ) * курс доллара к рублю
    """
    result = ((weight/1000) * 0.5 + cost_usd * 0.01) * usd_rate
    return round(result, 2)


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def calculate_delivery_cost_for_parcel() -> bool:
    logger.info("Calculating delivery cost for parcels")

    usd_rate = await get_current_usd_rate()
    logger.info(f"Rate USD/RUB: {usd_rate}")

    async with get_db_manager_null_pull() as db:
        parcels = await db.parcels.get_without_delivery_cost()
        if not parcels:
            logger.info("No parcels to update cost")
            return True
        logger.info(f"Parcels to update cost: {len(parcels)}")

        data_update = [
            ParcelUpdateCostDTO.model_validate(
                {"id": n.id, "delivery_cost": calc_cost(n.weight, n.cost_usd, usd_rate)}
            )
            for n in parcels
        ]
        res = await db.parcels.update_delivery_cost_batch(data_update)
        await db.commit()

        logger.info(f"Delivery cost sucessfully calculated for {res} parcels")
        return True
