from statistics import median
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select, and_
from database import new_session, TaskOrm
from repository import TaskRepository
from schemas import STaskAdd, STask, STaskId, STaskDates
import asyncio


router = APIRouter(
    prefix= '/tasks',
    tags=['Список команд']
)

#Эндпоинт на добавление таски
@router.post("")
async def add_task(
    task: Annotated[STaskAdd, Depends()],
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}

#Эндпоинт на получение всех данных в словаре
@router.get("")
async def get_tasks() -> list[STask]:
    tasks_orm = await TaskRepository.find_all()
    tasks = [STask(**task) for task in tasks_orm]
    return tasks


@router.get("/statistics")
async def get_statistics(date_range: STaskDates = Depends()):
    async with new_session() as session:
        query = select(TaskOrm).order_by(TaskOrm.timestamp)
        if date_range.start_date and date_range.end_date:
            query = query.where(
                and_(TaskOrm.timestamp >= date_range.start_date, TaskOrm.timestamp <= date_range.end_date))
        result = await session.execute(query)
        rows = result.all()

        # Extract x, y, z values from each row
        x_values = [row[0].x for row in rows]
        y_values = [row[0].y for row in rows]
        z_values = [row[0].z for row in rows]
        async def get_stat(var, var_name):
            return {"variable": var_name,
                    "min_value" : min(var) if var else None,
                    "max_value" : max(var) if var else None,
                    "count" : len(var) if var else None,
                    "sum" : sum(var) if var else None,
                    "median" :  await asyncio.to_thread(median, var) if var else None
                    }

        return await asyncio.gather(
            get_stat(x_values, "x"),
            get_stat(y_values,"y"),
            get_stat(z_values, "z")
        )