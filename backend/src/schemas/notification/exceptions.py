from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class CreateNotification422(ExceptionSchema):
    detail: Union[list, str] = Field(examples=['User id has not found'])
