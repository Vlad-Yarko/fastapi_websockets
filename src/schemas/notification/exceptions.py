from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class CreateNotification422(ExceptionSchema):
    detail: str = Field(examples=['User id has not found'])
