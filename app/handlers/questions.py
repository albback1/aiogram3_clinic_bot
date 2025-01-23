from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

import app.database.requests as rq
import app.keyboards as kb
import app.states as st
from config import GROUP_ID, LIMIT_TEXT_MESSAGE

question_router = Router()

"""
Вопрос специалисту клиники.

"""

@question_router.callback_query(F.data == "ask_doc")
async def get_ask_doc(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=(
            "Вы в конструкторе вопроса. " 
            "Следуйте инструкциям.\n" 
            "Примерное время ожидания ответа: 3 рабочих дня"
        ), 
        reply_markup=kb.ask_menu
    )

@question_router.callback_query(F.data == "start_ask")
async def ask_doc_init(callback: CallbackQuery, state: FSMContext):    
    await state.set_state(st.Specialists.specialist)
    await callback.answer()
    await callback.message.answer(
        text=(
            "Выберите специалиста, которому хотите задать вопрос, из меню ниже\n"
            "Если меню не появилось, нажмите на кнопку справа снизу"
        ), 
        reply_markup=kb.ask_kind_of_specialist
    )
    

@question_router.message(st.Specialists.specialist, F.text.in_(['Дерматологу', 'Терапевту', 'Ортопеду', 'Не знаю кому']))
async def ask_doc_get_specialist(message: Message, state: FSMContext):  
    await state.update_data(specialist=message.text)
    await state.set_state(st.Specialists.kind_of_pet)
    await message.answer(
        text=(
            "Выберите вид питомца.\n"
            "Если меню не появилось, нажмите на кнопку справа снизу"
        ), 
        reply_markup=kb.ask_kind_of_pet
    )

@question_router.message(st.Specialists.specialist)
async def fail_specialist(message: Message):
    await message.answer(
        text=(
            "Пожалуйста, используйте кнопки для выбора специалиста\n"
            "Если меню не появилось, нажмите на кнопку справа снизу"
        ), 
        reply_markup=kb.stop_fsm
    )

@question_router.message(st.Specialists.kind_of_pet, F.text.in_(['Кошка 🐈', 'Собака 🦮', 'Другое 🪿']))
async def ask_doc_get_pet(message: Message, state: FSMContext): 
    await state.update_data(kind_of_pet=message.text)
    await state.set_state(st.Specialists.text)
    await message.answer("Введите текст Вашего вопроса")

@question_router.message(st.Specialists.kind_of_pet)
async def fail_pet(message: Message):
    await message.answer(
        text=(
            "Пожалуйста, используйте кнопки для выбора вида питомца\n"
            "Если меню не появилось, нажмите на кнопку справа снизу"
        ), 
        reply_markup=kb.stop_fsm
    )

@question_router.message(st.Specialists.text, F.text)
async def ask_doc_get_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(st.Specialists.contact)
    await message.answer(
        text=(
            "Укажите желаемый способ связи. "
            "Если Вы хотите остаться в этом чате напишите 'чат', "
            "если Вам нужен обратный звонок, введите номер телефона."
        )
    )

@question_router.message(st.Specialists.text)
async def fail_text(message: Message):
    await message.answer(text="Пожалуйста, введите текстовое сообщение!") 

@question_router.message(st.Specialists.contact, F.text)
async def ask_doc_get_contact(message: Message, state: FSMContext):
    if len(message.text) > LIMIT_TEXT_MESSAGE:
        return await message.reply(
            text=(
                f"Превышен лимит. "
                f"Ваше сообщение слишком длинное: {len(message.text)} символов.\n" 
                f"Лимит: {LIMIT_TEXT_MESSAGE} символов."
            )
        )
    await state.update_data(contact=message.text)
    data = await state.get_data()
    await message.answer(
        text=(
            f"Пожалуйста, проверьте Ваш вопрос перед отправкой!\n"
            f"<i>Кому вопрос</i>: {data['specialist']}\n"
            f"<i>Вид животного</i>: {data['kind_of_pet']}\n"
            f"<i>Текст вопроса</i>: {data['text']}\n"
            f"<i>Способ связи</i>: {data['contact']}\n"     
        ), 
        parse_mode=ParseMode.HTML,
        reply_markup=kb.get_ask
    )

"""
@router.message(SupportedMediaFilter(), F.chat.type == 'private')
async def supported_media(message: Message):
    if message.caption and len(message.caption) > 1000:
        return await message.reply(text='Слишком длинное описание. Описание '
                                        'не может быть больше 1000 символов')
    await message.copy_to(
        chat_id=settings.GROUP_ID,
        caption=((message.caption or "") +
                 f"\n\n Тикет: #id{message.from_user.id}"),
        parse_mode="HTML"
    )
    session_generator = get_async_session()
    session = await session_generator.__anext__()
    db_user = await crud_user.get_or_create_user_by_tg_message(message, session)
    if check_user_is_banned(db_user):
        return
    message_data = {
        'telegram_user_id': message.from_user.id,
        'attachments': True,
    }
    if message.caption:
        message_data['text'] = message.caption
    await crud_message.create(message_data, session)

"""


@question_router.message(st.Specialists.contact)
async def fail_contact(message: Message):
    await message.answer("Принимается только текст!") 

# если добавить прием медиа, то в бд 

@question_router.callback_query(F.data == "push")
async def ask_doc_get_permission(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await callback.answer()
    await callback.message.answer(
        text=(
            "Ваш вопрос направлен нашим специалистам!\n"
            "Время ожидания...\n"
        ),
        reply_markup=ReplyKeyboardRemove())

    await callback.message.answer(
        text=(
            "<b>ВНИМАНИЕ!</b> Данная форма <i>не является прямым чатом</i> со специалистом. " 
            "Ваши последующие сообщения не будут переданы специалистам.\n"
            "Если у Вас остались вопросы, Вы можете записаться в клинику для подробной консультации"
        ), 
        parse_mode=ParseMode.HTML,
        reply_markup=kb.back_to_menu
    )

    await rq.set_question(callback.from_user.id, data['specialist'], data['text'])

    await bot.send_message(
        chat_id=GROUP_ID,
        text=(
            f"<i>Кому вопрос</i>: #{data['specialist']}\n"
            f"<i>Вид животного</i>: {data['kind_of_pet']}\n"
            f"<i>Текст вопроса</i>:\n{data['text']}\n"
            f"<i>Способ связи</i>: {data['contact']}\n"
            f"<i>От</i>: @{callback.from_user.username} | #id{callback.from_user.id}"
        ), parse_mode=ParseMode.HTML
    )
    await state.clear()
