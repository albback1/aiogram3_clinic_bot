from aiogram.utils.keyboard import InlineKeyboardBuilder

def add_pagination_buttons(builder, page: int, total_pages: int, prefix: str, category_id: int = None):
    """
    Добавляет кнопки пагинации в клавиатуру.

    Args:
        builder (InlineKeyboardBuilder): Объект для построения клавиатуры.
        page (int): Текущая страница.
        total_pages (int): Общее количество страниц.
        prefix (str): Префикс для callback_data (например, "cat", "item").
        category_id (int, optional): ID категории. Используется для формирования callback_data.

    Returns:
        None: Функция изменяет объект builder, добавляя кнопки пагинации.

    """

    # Кнопка "Назад"
    # Отображается всегда, но если страниц дальше нет, 
    # то имеет другой callback data
    if page > 1:
        callback_data = f"{prefix}_page_{page - 1}"
        if category_id is not None:
            callback_data += f"_{category_id}"
        builder.button(text="⬅️", callback_data=callback_data)
    elif page == 1:
        builder.button(text="⬅️", callback_data="on_first_page")

    # Кнопка "Вперед"
    # Отображается всегда, но если страниц дальше нет, 
    # то имеет другой callback data
    if page < total_pages:
        callback_data = f"{prefix}_page_{page + 1}"
        if category_id is not None:
            callback_data += f"_{category_id}"
        builder.button(text="➡️", callback_data=callback_data)
    elif page == total_pages:
        builder.button(text="➡️", callback_data="on_last_page")

def create_paginated_keyboard(items, page: int, total_pages: int, prefix: str, back_callback: str = None, to_main_callback: str = "to_main"):
    """
    Создает клавиатуру с пагинацией.

    Функция создает инлайн-клавиатуру с кнопками для навигации между страницами.
    Добавляется кнопка возврата на категорию назад, если это необходимо.
    Добавляется кнопка возврата а главное меню.

    Args:
        items (list): Список элементов для отображения на текущей странице.
        page (int): Текущая страница.
        total_pages (int): Общее количество страниц.
        prefix (str): Префикс для callback_data (например, "cat", "item").
        back_callback (str, optional): Callback_data для кнопки "Назад". Если не указано, кнопка не добавляется.
        to_main_callback (str): Callback_data для кнопки "В главное меню". По умолчанию "to_main".

    Returns:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками пагинации.
    """
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(text=item.name, callback_data=f"{prefix}_{item.id}")

    add_pagination_buttons(builder, page, total_pages, prefix)

    if back_callback:
        builder.button(text="🔙 Вернуться", callback_data=back_callback)

    builder.button(text="В главное меню 🏠", callback_data=to_main_callback)

    builder.adjust(1, 1, 1, 1, 2, 2, 2, 1) # Подбирается индивидуально для удобного отображения
    return builder.as_markup()


    