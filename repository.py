# Описываю взаимодействие с базой данных
from datetime import datetime

from database import  new_session, TaskOrm
from sqlalchemy import select

from schemas import STaskAdd


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