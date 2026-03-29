from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func
from datetime import datetime, timezone
from app.models.task import Task
from app.schemas.task_schema import TaskCreate

class TaskRepository:
    @staticmethod
    def create(db: Session, task_in: TaskCreate, user_id: int):
        db_task = Task(**task_in.model_dump(), user_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_all_active(db: Session, user_id: int, skip: int, limit: int):
        stmt = select(Task).filter(
            and_(Task.user_id == user_id, Task.deleted_at == None)
        ).offset(skip).limit(limit)
        
        count_stmt = select(func.count()).select_from(Task).filter(
            and_(Task.user_id == user_id, Task.deleted_at == None)
        )
        
        tasks = db.execute(stmt).scalars().all()
        total = db.execute(count_stmt).scalar()
        return tasks, total

    @staticmethod
    def update_status(db: Session, task_id: int, user_id: int, status: str):
        stmt = select(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id, Task.deleted_at == None)
        )
        task = db.execute(stmt).scalar_one_or_none()
        
        if task:
            task.status = status
            db.commit()
            db.refresh(task)
        return task

    @staticmethod
    def soft_delete(db: Session, task_id: int, user_id: int):
        stmt = select(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id, Task.deleted_at == None)
        )
        task = db.execute(stmt).scalar_one_or_none()
        
        if task:
            task.deleted_at = datetime.now(timezone.utc)
            db.commit()
            return True
        return False