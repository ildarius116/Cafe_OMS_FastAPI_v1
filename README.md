# Система управления заказами в кафе на фреймворке FastAPI

_Техническое задание:_
```text
Исходный проект из https://github.com/ildarius116/Cafe_OMS_Django, переделал на фреймворк FastAPI
```


__Доступные адреса (эндпоинты) и функции:__


* `/` - адрес отображения списка заказов
* `/<int:pk>/` - адрес просмотра и редактирования деталей заказа
* `/<int:pk>/edit/` - адрес просмотра и редактирования статуса заказа
* `/<int:pk>/delete/` - адрес POST-запроса на удаление заказа
* `/new/` - адрес страницы создания нового заказа 
* `/revenue/` - адрес просмотра отчета о выручке
* `/menu-item/new/` - адрес создания элемента (блюда) Меню - **_в разработке (опциональная функция)_**
* `/api/v1/orders/` - адрес API-функционала CRUD операций с заказами
* `/api/v1/menu_items/` - адрес API-функционала CRUD операций с Меню
* `/api/v1/association/` - адрес API-функционала CRUD операций со связями m2m (Заказы - элементы Меню)
* `/api/schema/` - адрес yaml-схемы API-функционала
* `/api/docs/` - адрес swagger-схемы API-функционала
* `/api/redoc/` - адрес redoc-схемы API-функционала


## Примеры:

* #### _Отображение списка заказов:_
* ![orders_list.JPG](README%2Forders_list.JPG)
* #### _Детали заказа:_
* ![order_detals_pending.JPG](README%2Forder_detals_pending.JPG)
* ![order_detals_add.png](README%2Forder_detals_add.png)
* #### _Обновление статуса заказа:_
* ![update_status.JPG](README%2Fupdate_status.JPG)
* #### _Создание нового заказа:_
* ![create_order.JPG](README%2Fcreate_order.JPG)
* #### _Просмотр отчета о выручке:_
* ![revenue.JPG](README%2Frevenue.JPG)
* #### _Создание элемента (блюда) Меню (не было в ТЗ):_
* ![menu_item_add.JPG](README%2Fmenu_item_add.JPG)
* #### _Swagger API:_
* ![api.JPG](README%2Fapi.JPG)


## Порядок запуска:
* Клонировать: `git clone https://github.com/ildarius116/Cafe_OMS_FastAPI_v1`
* Установить зависимости: `pip install poetry`
* Установить зависимости: `poetry install`
* Создать миграции: `alembic revision --autogenerate -m "initial"`
* Применить миграции: `alembic upgrade head`
* Запустить сервер: `uvicorn src.main:app`


### _Примечания:_
1. По необходимости, запустить тесты, командой: `pytest`
* ![tests.JPG](README%2Ftests.JPG)
2. По необходимости, создайте тестовые данные заказов и блюд: `xxx` - **_в разработке_**
