from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, select
from datetime import datetime

engine = create_async_engine(
    "sqlite+aiosqlite:///tasks.db"
) # Создал асинхронный движок (Название бд, драйвер, название файла
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

#описываю модель таблицы (БД)
class TaskOrm(Model):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id : Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=func.datetime())
    x : Mapped[float] = mapped_column()
    y : Mapped[float] = mapped_column()
    z : Mapped[float] = mapped_column()
# Создаю функцию для создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await  conn.run_sync(Model.metadata.drop_all)
