from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           WebAppInfo)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.pagination import add_pagination_buttons, create_paginated_keyboard


# Клавиатура для главного меню.

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Записаться в клинику 📅", callback_data="enroll")],
    [InlineKeyboardButton(text="Прайс-лист 📃", callback_data="price_list")],
    [InlineKeyboardButton(text="Задать вопрос специалисту ❔", callback_data="ask_doc")]
])

back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В главное меню 🏠", callback_data="to_main")]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")]
])

stop_fsm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отменить и выйти ❌", callback_data="cancel")]
])


# Клавиатура для меню записи.
enrolling = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Позвоните мне 📞", callback_data="call_me")],
    [InlineKeyboardButton(text="Онлайн-запись 📱", web_app=WebAppInfo(url='https://example.com/'))],
    [InlineKeyboardButton(text="В главное меню 🏠", callback_data="to_main")]
])

branch = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="На [улица 1]")],
    [KeyboardButton(text="На [улица 2]")]
]) 



# Клавиатуры для прайс-листа. Пагинация.

def create_category_keyboard(categories, page: int, total_pages: int):
    """
    Create a paginated keyboard for categories.
    """
    return create_paginated_keyboard(
        items=categories,
        page=page,
        total_pages=total_pages,
        prefix="cat",
        back_callback=None,  # Нет необходимости, т.к. предыдущее меню - главное
        to_main_callback="to_main"
    )

def create_item_keyboard(page: int, total_pages: int, category_id: int = None):
    """
    Создает клавиатуру для услуг с пагинацией.

    :param page: Текущая страница.
    :param total_pages: Общее количество страниц.
    :param category_id: ID категории (опционально).
    :return: InlineKeyboardMarkup.
    """
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки пагинации
    add_pagination_buttons(builder, page, total_pages, "item", category_id)

    # Добавляем кнопку "Назад"
    if category_id:
        builder.button(text="🔙 Вернуться", callback_data=f"back_to_categories_{category_id}")

    # Добавляем кнопку "В главное меню"
    builder.button(text="В главное меню 🏠", callback_data="to_main")

    # Настраиваем расположение кнопок
    builder.adjust(2, 1)
    return builder.as_markup()


# Клавиатуры для составления вопроса специалисту
ask_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Написать вопрос 📝", callback_data="start_ask")],
    [InlineKeyboardButton(text="В главное меню 🏠", callback_data="to_main")]
])

ask_kind_of_specialist = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Дерматологу")],
    [KeyboardButton(text="Терапевту")],
    [KeyboardButton(text="Ортопеду")],
    [KeyboardButton(text="Не знаю кому")], 
    [KeyboardButton(text="Отмена ❌")]
], one_time_keyboard=True)


ask_kind_of_pet = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Кошка 🐈")],
    [KeyboardButton(text="Собака 🦮")],
    [KeyboardButton(text="Другое 🪿")], 
    [KeyboardButton(text="Отмена ❌")]
], one_time_keyboard=True)

get_ask = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подтвердить ✅", callback_data="push")],
    [InlineKeyboardButton(text="Отменить и выйти ❌", callback_data="cancel")]
])
