from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class CreateUser422(ExceptionSchema):
    detail: Union[str, list] = Field(examples=['Username has already found'])
    
    
class LoginUser422(ExceptionSchema):
    detail: Union[str, list] = Field(examples=['Username has not found'])
    

class LoginUser400(ExceptionSchema):
    detail: Union[str, list] = Field(examples=['User is already authenticated. Refresh token has found'])
    
    
class Token400(ExceptionSchema):
    detail: Union[str, list] = Field(examples=['Token id or user id has not found'])
    
    
class Token403(ExceptionSchema):
    detail: Union[str, list] = Field(examples=['User is not authenticated. Refresh token has not found'])
    
    
class Token422(ExceptionSchema):
    detail: Union[str, list] = Field(examples=['Invalid token'])
    
    
class GetUser422(ExceptionSchema):
    detail: Union[str, list] = Field(examples=["Id has not found"])
