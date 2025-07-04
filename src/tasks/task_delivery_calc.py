import logging
from exceptions import ParcelNotFoundException
from repository.parcels import ParcelsRepository
from src.api.dependencies import get_db_manager_null_pull
from src.tasks.celery import celery_app
from src.tasks.task_exchange import get_current_usd_rate

logger = logging.getLogger(__name__)


async def calculate_delivery_cost_for_parcel(parcel_id: int) -> bool:
    """
    Celery task to calc delyvery cost
    Args:
        parcel_id: int
    Returns:
        bool: True if succes, False on error
    """
    try:
        logger.info(f"Calculating delivery cost for parcel ID: {parcel_id}")
        
        usd_rate = await get_current_usd_rate()
        logger.info(f"Rate USD/RUB: {usd_rate}")
        
        async with get_db_manager_null_pull() as db:
            parcel = await db.parcels.get_by_id_wo_session(parcel_id)
                
            delivery_cost = (parcel.weight * 0.5 + parcel.cost_usd * 0.01) * usd_rate
            
            logger.info(
                f"Delivery calculation ID {parcel_id}: "
                f"weight={parcel.weight}gramms, cost={parcel.cost_usd}$, "
                f"rate={usd_rate}, total={delivery_cost:.2f}₽"
            )

            await db.parcels.update_delivery_cost(parcel_id, delivery_cost)
            await db.commit()
            
            logger.info(f"Delivery cost for ID {parcel_id} sucessfully calculated: {delivery_cost:.2f}₽")
            return True
    except ParcelNotFoundException as e:
        logger.error(f"Parsel not found or already calculated ID {parcel_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Something went wrong ID {parcel_id}: {e}")
        return False
    


# @celery_app.task(bind=True)
