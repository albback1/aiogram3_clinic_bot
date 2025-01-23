from aiogram import Router
from aiogram.types import CallbackQuery

fallback_router = Router()

# Отлавливание необрабатываемых callback data
@fallback_router.callback_query()
async def fallback_handler(callback: CallbackQuery):
    print(f"Unhandled callback data: {callback.data}")  
    await callback.answer("Данное действие не поддерживается")