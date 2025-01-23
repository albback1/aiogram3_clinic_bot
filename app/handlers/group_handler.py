from aiogram import F, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.types import Message

import app.database.requests as rq
from app.func_convert_data import convert_to_moscow_time

group_router = Router()

# Взаимодействие бота с чатом поддержки.
# Ответ юзеру по id через бота из группового чата. 
# Ответивший остается анонимным.
@group_router.message(F.chat.type == "supergroup", F.reply_to_message)
async def send_message_answer(message: Message):
    if not message.reply_to_message.from_user.is_bot:
        return
    try:
        text = message.reply_to_message.text
        chat_id = text.split(sep='#id')[-1]
    except ValueError as err:
        return await message.reply(text=f"Не могу извлечь ID. "
                                        f"Ошибка:\n"
                                        f"{str(err)}")
    try:
        await message.copy_to(chat_id)
    except TelegramForbiddenError:
        await message.reply(text="Сообщение не доставлено. Бот был "
                                 "заблокировн пользователем, "
                                 "либо пользователь удален")

# Получения списка всех заданных вопросов
@group_router.message(F.chat.type == "supergroup", Command('list'))
async def get_list_of_questions(message: Message):
    questions = await rq.get_question()
    if not questions:
        await message.answer("Вопросов пока нет.")
        return
    
    # Форматирование времени
    for question in questions:    
        moscow_time = convert_to_moscow_time(question.created_at)
        created_at_str = moscow_time.strftime("%Y-%m-%d %H:%M")

    message_text = "Список вопросов:\n"
    for question in questions:
        message_text += (
            f"№ {question.id}.\n"
            f"Специалист: {question.specialist}\n"
            f"Текст вопроса: {question.text}\n"
            f"Дата создания: {created_at_str} МСК\n"
            "--------------------------\n"
        )

    await message.answer(text=message_text)