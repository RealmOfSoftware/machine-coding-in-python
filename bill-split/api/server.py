from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from api import controller
import exceptions

app = FastAPI()
app.include_router(controller.router)


@app.exception_handler(exceptions.AlreadyExists)
def already_exists_exception_handler(request, exc):
    return error_response(exc, 400)


@app.exception_handler(exceptions.DoesNotExists)
def does_not_exists_exception_handler(request, exc):
    return error_response(exc, 404)


@app.exception_handler(exceptions.InvalidBill)
def invalid_bill_exception_handler(request, exc):
    return error_response(exc, 400)


def error_response(exc: Exception, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={"message": str(exc), "type": exc.__class__.__name__},
    )
