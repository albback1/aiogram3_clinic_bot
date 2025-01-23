from aiogram import F, Router

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.database.requests as rq
import app.keyboards as kb

common_router = Router()

"""
Обработчики для: 
- команды '/start'
- кнопки возврата в меню
- остановки FSM

"""

@common_router.message(F.chat.type == 'private', CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!", 
                         reply_markup=kb.main_menu)

@common_router.callback_query(F.data == "to_main")
async def to_main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"Вы вернулись в главное меню", 
                                     reply_markup=kb.main_menu)
    
@common_router.callback_query(F.data == "cancel")
async def stop_fsm_private(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer(f"Сценарий остановлен. Вы вернулись в главное меню",
                                  reply_markup=kb.main_menu)


