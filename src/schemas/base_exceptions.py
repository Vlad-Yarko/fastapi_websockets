from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class Authentication401(ExceptionSchema):
    detail: str = Field(examples=["Bearer token is invalid"])
