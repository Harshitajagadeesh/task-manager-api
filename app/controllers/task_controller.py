from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.schemas.task_schema import (
    TaskCreate, 
    TaskUpdate, 
    SingleTaskResponse, 
    TaskListResponse
)
from app.services.task_service import TaskService
from app.middlewares.auth_middleware import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=SingleTaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate, 
    db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user)
):
    task = TaskService.create_task(db, task_in, user_id)
    return {
        "success": True, 
        "message": "Task created successfully", 
        "data": task
    }

@router.get("/", response_model=TaskListResponse)
def get_all_tasks(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, le=100), 
    db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user)
):
    result = TaskService.get_user_tasks(db, user_id, skip, limit)
    return {
        "success": True, 
        "message": "Tasks retrieved successfully", 
        "data": result["tasks"]
    }

@router.patch("/{task_id}", response_model=SingleTaskResponse)
def update_task_status(
    task_id: int, 
    update_in: TaskUpdate, 
    db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user)
):
    task = TaskService.update_task_status(db, task_id, user_id, update_in)
    return {
        "success": True, 
        "message": f"Status updated to {update_in.status}", 
        "data": task
    }

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user)
):
    TaskService.delete_task(db, task_id, user_id)
    return {
        "success": True, 
        "message": "Task deleted successfully", 
        "data": None
    }