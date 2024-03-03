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

async def sum_x() -> float:
    async with new_session() as session:
        query = select(func.sum(TaskOrm.x))
        result = await session.execute(query)
        total_sum = result.scalar()
        return total_sum


def get_stats(session,start_date = None, end_date = None):
    query = (
        select(
            func.min(TaskOrm.x).label("min_x"),
            func.max(TaskOrm.x).label("max_x"),
            func.count(TaskOrm.x).label("count_x"),
            func.sum(TaskOrm.x).label("sum_x"),
            func.median(TaskOrm.x).label("median_x"),
            func.min(TaskOrm.y).label("min_y"),
            func.max(TaskOrm.y).label("max_y"),
            func.count(TaskOrm.y).label("count_y"),
            func.sum(TaskOrm.y).label("sum_y"),
            func.median(TaskOrm.y).label("median_y"),
            func.min(TaskOrm.z).label("min_z"),
            func.max(TaskOrm.z).label("max_z"),
            func.count(TaskOrm.z).label("count_z"),
            func.sum(TaskOrm.z).label("sum_z"),
            func.median(TaskOrm.z).label("median_z"),
        )
    )

    if start_date is not None and end_date is not None:
        query = query.where(and_(TaskOrm.timestamp >= start_date, TaskOrm.timestamp <= end_date))


    result = session.execute(query).first()
    return result