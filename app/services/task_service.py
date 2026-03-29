from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    def create_task(db: Session, task_in: TaskCreate, user_id: int):
        return TaskRepository.create(db, task_in, user_id)

    @staticmethod
    def get_user_tasks(db: Session, user_id: int, skip: int, limit: int):
        tasks, total = TaskRepository.get_all_active(db, user_id, skip, limit)
        return {
            "tasks": tasks,
            "total": total,
            "skip": skip,
            "limit": limit
        }

    @staticmethod
    def update_task_status(db: Session, task_id: int, user_id: int, update_in: TaskUpdate):
        task = TaskRepository.update_status(db, task_id, user_id, update_in.status)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found or access denied"
            )
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int, user_id: int):
        success = TaskRepository.soft_delete(db, task_id, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found or access denied"
            )
        return True