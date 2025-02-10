# api/cruds/task.py

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import api.models.task as task_model
from api.schemas.task import TaskCreate
from api.model_inference import run_model

async def create_task(db: AsyncSession, task_body: TaskCreate) -> task_model.Task:
    # 非同期環境下でブロッキングなrun_modelを実行するため、to_threadで実行
    result_text = await asyncio.to_thread(run_model, task_body.query)
    new_task = task_model.Task(query=task_body.query, result=result_text)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

async def get_tasks_with_done(db: AsyncSession):
    result = await db.execute(select(task_model.Task))
    tasks = result.scalars().all()
    return tasks

async def get_task(db: AsyncSession, task_id: int):
    task = await db.get(task_model.Task, task_id)
    return task

async def update_task(db: AsyncSession, task_body: TaskCreate, original: task_model.Task) -> task_model.Task:
    original.query = task_body.query
    # 再度モデル実行して更新する
    original.result = await asyncio.to_thread(run_model, task_body.query)
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()