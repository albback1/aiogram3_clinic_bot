from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

import app.database.requests as rq
import app.keyboards as kb

price_router = Router()


# Прайс лист.
# Пагинация, базы данных

@price_router.callback_query(F.data == "price_list")
async def show_categories(callback: CallbackQuery):
    # Данные из БД для первой страницы
    page = 1
    categories = await rq.get_categories(page)
    total_pages = await rq.get_total_pages(rq.Category)

    keyboard = kb.create_category_keyboard(categories, page, total_pages)

    # Обновление сообщения
    await callback.message.edit_text(
        text=(
            "<i>Выберите категорию:</i>"
        ),
        parse_mode=ParseMode.HTML, 
        reply_markup=keyboard
    )

@price_router.callback_query(F.data.startswith("cat_page_"))
async def on_category_page(callback: CallbackQuery):
    try:
        page = int(callback.data.split("_")[2])  # Extract page number from callback data
    except (IndexError, ValueError) as e:
        print(f"Error parsing callback data: {e}")
        return

    categories = await rq.get_categories(page)
    total_pages = await rq.get_total_pages(rq.Category)

    keyboard = kb.create_category_keyboard(categories, page, total_pages)

    await callback.message.edit_text(
        text=(
            "<i>Выберите категорию:</i>"
        ),
        parse_mode=ParseMode.HTML,  
        reply_markup=keyboard
    )

async def handle_items_page(callback: CallbackQuery, category_id: int, page: int):
    """
    Обрабатывает отображение страницы с услугами.

    :param callback: Объект CallbackQuery.
    :param category_id: ID категории.
    :param page: Текущая страница.
    """
    # Запрос в БД
    items = await rq.get_items(category_id=category_id, page=page)
    total_pages = await rq.get_total_pages(rq.Item, filter_by={"category_id": category_id})

    # Форматирование
    items_text = "\n".join([f"<b>{item.name}</b> - {item.price} руб." for item in items])
    message_text = f"<i>Услуги (страница {page} из {total_pages}):</i>\n\n{items_text}"

    # Клавиатура
    keyboard = kb.create_item_keyboard(page, total_pages, category_id=category_id)

    # Обновление сообщения
    await callback.message.edit_text(
        text=message_text,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@price_router.callback_query(F.data.startswith("cat_"))
async def on_category_select(callback: CallbackQuery):
    # Исключение callback data пагинации
    if callback.data.startswith("cat_page_"): 
        return  

    try:
        # Выделение номера страницы из callback data
        category_id = int(callback.data.split("_")[1])  
    except (IndexError, ValueError) as e:
        print(f"Error parsing callback data: {e}")
        return

    # Обработка первой страницы
    await handle_items_page(callback, category_id, page=1)


@price_router.callback_query(F.data.startswith("item_page_"))
async def on_item_page(callback: CallbackQuery):
    try:
        # Выделение номера страницы из callback data
        data_parts = callback.data.split("_")
        page = int(data_parts[2])
        category_id = int(data_parts[3]) if len(data_parts) > 3 and data_parts[3] != "None" else None
    except (IndexError, ValueError) as e:
        print(f"Error parsing callback data: {e}")
        return

    # Обработка страницы
    await handle_items_page(callback, category_id, page)

# Обработка кнопки "назад" на первой странице
@price_router.callback_query(F.data == "on_first_page")
async def on_first_page(callback: CallbackQuery):
    await callback.answer("Вы на первой странице.")

# Обработка кнопки "вперед" на последней странице
@price_router.callback_query(F.data == "on_last_page")
async def on_first_page(callback: CallbackQuery):
    await callback.answer("Вы на последней странице.")


@price_router.callback_query(F.data.startswith("back_to_categories"))
async def on_back_to_categories(callback: CallbackQuery):
    # Первая страница категорий
    page = 1
    categories = await rq.get_categories(page)
    total_pages = await rq.get_total_pages(rq.Category)

    # Клавиатура для категорий
    keyboard = kb.create_category_keyboard(categories, page, total_pages)

    # Обновление сообщения
    await callback.message.edit_text(
        text="<i>Выберите категорию:</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )