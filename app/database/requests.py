from sqlalchemy import func, select

from app.database.models import (Category, Item, Question, User,
                                 async_session)


async def set_user(tg_id: int, username: str, full_name: str):
    """Добавление пользователя в БД"""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username, full_name=full_name))
            await session.commit()


async def set_question(tg_id: int, specialist: str, text: str):
    """Добавление вопроса в БД"""
    async with async_session() as session:
        new_question = Question(
            tg_id=tg_id, 
            specialist=specialist,
            text=text
        )
        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)  # Обновление объекта, для получения его ID и др. полей
        return new_question

async def get_question():
    """Получение списка вопросов из БД"""
    async with async_session() as session:
        result = await session.execute(select(Question))
        return result.scalars().all()


async def get_categories(page: int, per_page: int = 8):
    """Получение категорий из БД с учетом пагинации"""
    async with async_session() as session:
        offset = (page - 1) * per_page
        result = await session.execute(
            select(Category)
            .offset(offset)
            .limit(per_page)
        )
        return result.scalars().all()

  
async def get_items(category_id: int = None, page: int = 1, per_page: int = 10):
    """Получение данных об услугах из БД с учетом пагинации"""
    async with async_session() as session:
        offset = (page - 1) * per_page
        query = select(Item)
        query = query.filter(Item.category_id == category_id)

        # ограничение строк на странице
        query = query.offset(offset).limit(per_page)
        
        result = await session.execute(query)
        items = result.scalars().all()

        return items


async def get_total_pages(model, filter_by=None, per_page: int = 8):
    """Количество страниц для пагинации"""
    async with async_session() as session:
        query = select(model)
        if filter_by:
            query = query.filter_by(**filter_by)
        total_items = await session.scalar(select(func.count()).select_from(query))
        total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
        return total_pages