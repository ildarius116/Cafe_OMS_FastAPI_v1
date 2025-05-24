import asyncio
import logging

from src.actions.create_orders import create_orders, orders_data
from src.actions.create_menu_items import create_menu_items, menu_items_data
from src.actions.create_associations import create_associations
from src.core.models import db_helper

log = logging.getLogger(__name__)


if __name__ == "__main__":
    orders_data = orders_data()
    menu_items_data = menu_items_data()
    session = db_helper.get_scoped_session()
    asyncio.run(create_orders(session=session, orders_data=orders_data))
    asyncio.run(create_menu_items(session=session, menu_items_data=menu_items_data))
    asyncio.run(create_associations(session=session))
