from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger("uvicorn.error")

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = [
        {"field": ".".join(map(str, err["loc"][1:])), "message": err["msg"]}
        for err in exc.errors()
    ]
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": error_details
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal Server Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error. Please contact support.",
            "data": None
        }
    )