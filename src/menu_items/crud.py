from src.menu_items.schemas import MenuItemSchema, MenuItemsSchema


def create_menu_item(item: MenuItemSchema):
    menu_item = item.model_dump()
    message = {
        "message": "create_menu_item",
        "success": True,
        "menu_item": menu_item,
    }
    # return message
    return item


def read_menu_item(MenuItemSchema):
    ...


def list_menu_items(MenuItemSchema):
    ...


def update_menu_item(MenuItemSchema):
    ...


def delete_menu_item():
    ...
