from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.config.database import engine, Base
from app.controllers import user_controller, task_controller
from app.middlewares.exception import (
    validation_exception_handler, 
    generic_exception_handler
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Task Management API",
    description="A professional RESTful API with JWT Auth and PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(user_controller.router)
app.include_router(task_controller.router)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "success": True,
        "message": "Task Management API is operational",
        "version": "1.0.0"
    }