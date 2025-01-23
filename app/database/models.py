from sqlalchemy import BigInteger, DateTime, Column, ForeignKey, func, Integer, String
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, relationship

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

# Таблица для хранения данных о пользователях бота
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger)
    username = Column(String(220), nullable=True)
    full_name = Column(String(220), nullable=True)


# Таблица для хранения вопросов
class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger)
    specialist = Column(String(50))
    text = Column(String(4000))
    created_at = Column(DateTime, default=func.now())  # Дата и время по UTC 


# Таблицы прайс-листа
# 1. Категории
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    items = relationship("Item", back_populates="category")

# 2. Подкатегории
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String) # т.к. есть записи в виде "от 3000"
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="items")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)