from pydantic import Field

from src.utils.schema import Schema


class User(Schema):
    username: str = Field(examples=['mister_business'], min_length=2, max_length=50)


class UserPublic(User):
    id: int = Field(examples=[1])
    
    model_config = {
        "extra": "ignore"
    }


class UserBody(User):
    password: str = Field(examples=['12345678'], min_length=8, max_length=70)


class Token(Schema):
    accessToken: str = Field(..., examples=['asfnbmbmbewrqdijhdsfafgsdhhvbxcbfgerydgsfgagf'])


class TokenPublic(Token):
    pass
