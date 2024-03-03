# Описываю взаимодействие с базой данных
from datetime import datetime
from statistics import median
from typing import Optional

from database import  new_session, TaskOrm
from sqlalchemy import select, func, and_

from schemas import STaskAdd, STask


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd):
        async with new_session() as session:
            task_dict = data.model_dump()
            task_dict['timestamp'] = datetime.utcnow()
            task = TaskOrm(**task_dict)
            session.add(task)   # Добавляем новый объект в сессию
            await session.flush()
            await session.commit() # Вносим все изменения в БД
            return task.id


    @classmethod
    async def find_all(cls) -> list[dict]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_dicts = [task_model.__dict__ for task_model in task_models]
            return task_dicts

    @classmethod
    async def get_stats(cls, start_date=None, end_date=None):
        async with new_session() as session:
            return await get_stats(session, start_date, end_date)


async def get_stats(session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    query = (
        select(
            func.min(TaskOrm.x).label("min_x"),
            func.max(TaskOrm.x).label("max_x"),
            func.count(TaskOrm.x).label("count_x"),
            func.sum(TaskOrm.x).label("sum_x"),
            func.min(TaskOrm.y).label("min_y"),
            func.max(TaskOrm.y).label("max_y"),
            func.count(TaskOrm.y).label("count_y"),
            func.sum(TaskOrm.y).label("sum_y"),
            func.min(TaskOrm.z).label("min_z"),
            func.max(TaskOrm.z).label("max_z"),
            func.count(TaskOrm.z).label("count_z"),
            func.sum(TaskOrm.z).label("sum_z"),
        )
    )

    if start_date is not None and end_date is not None:
        query = query.where(and_(TaskOrm.timestamp >= start_date, TaskOrm.timestamp <= end_date))

    result = await session.execute(query)
    row = await result.fetchone()


    stats = {
        "min_x": row["min_x"],
        "max_x": row["max_x"],
        "count_x": row["count_x"],
        "sum_x": row["sum_x"],
        "median_x": median(row["min_x"], row["max_x"], row["sum_x"] / row["count_x"]),
        "min_y": row["min_y"],
        "max_y": row["max_y"],
        "count_y": row["count_y"],
        "sum_y": row["sum_y"],
        "median_y": median(row["min_y"], row["max_y"], row["sum_y"] / row["count_y"]),
        "min_z": row["min_z"],
        "max_z": row["max_z"],
        "count_z": row["count_z"],
        "sum_z": row["sum_z"],
        "median_z": median(row["min_z"], row["max_z"], row["sum_z"] / row["count_z"]),
    }

    return stats
