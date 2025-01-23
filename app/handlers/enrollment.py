from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

import app.keyboards as kb
import app.states as st
from config import GROUP_ID

enroll_router = Router()

"""
Запись в клинику:
    - Переход на сайт
    - Заказ обратного звонка

"""

@enroll_router.callback_query(F.data == "enroll")
async def get_enroll(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=(
            "Вы можете записаться на прием через <u>наш сайт</u> "
            "или <u>заказать звонок</u>.\n"
            "Выберите необходимое из меню: "
        ),
        parse_mode=ParseMode.HTML, 
        reply_markup=kb.enrolling
        )

@enroll_router.callback_query(F.data == "call_me")
async def reg_call_init(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.Phone.get_branch)
    await callback.answer()
    await callback.message.answer(text="Выберите филиал по кнопкам ниже:", 
                                  reply_markup=kb.branch)

@enroll_router.message(st.Phone.get_branch, F.text.in_(['На [улица 1]', 'На [улица 2]']))
async def reg_call_branch(message: Message, state: FSMContext):  
    await state.update_data(get_branch=message.text)
    await state.set_state(st.Phone.name)
    await message.answer(text="Как к Вам обращаться?", 
                         reply_markup=ReplyKeyboardRemove())

@enroll_router.message(st.Phone.get_branch)
async def fail_reg_call_branch(message: Message):
    await message.answer(text=(
        "Пожалуйста, используйте <i>кнопки для выбора филиала</i>"
        ), 
        reply_markup=kb.stop_fsm)

@enroll_router.message(st.Phone.name)
async def reg_call_number(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.Phone.number)
    await message.answer(
        text=(
            "Введите номер телефона для связи\n"
            "Формат: <u>+7xxx-xxx-xx-xx</u>"
        ),
        parse_mode=ParseMode.HTML 
        )

@enroll_router.message(st.Phone.number)
async def reg_call_end(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(
        text=(
            f"<b>Спасибо! Свяжемся с Вами в ближайшее время!</b>\n"
            f"Филиал: {data['get_branch']}\n"
            f"Имя: {data['name']}\n"
            f"Номер: {data['number']}\n"
            f"От: @{message.from_user.username}"
        ),
        parse_mode=ParseMode.HTML, 
        reply_markup=kb.back_to_menu)
    
    await bot.send_message(
        chat_id=GROUP_ID,
        text=(
            f"<b>ОБРАТНЫЙ ЗВОНОК ДЛЯ ЗАПИСИ!</b>\n"
            f"<i>Филиал</i>: {data['get_branch']}\n"
            f"<i>Имя</i>: {data['name']}\n"
            f"<i>Номер</i>: {data['number']}\n"
            f"<i>От</i>: @{message.from_user.username}"
        ), parse_mode=ParseMode.HTML)
    
    await state.clear()