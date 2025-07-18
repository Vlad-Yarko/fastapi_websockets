from fastapi import APIRouter

from src.schemas.base_exceptions import Authentication403
from src.schemas.user import UserPublic, TokenPublic, CreateUser422, LoginUser422, LoginUser400, Token400, Token403, Token422, GetUser422
from src.api.dependencies.user import CreatedUser, LoginUser, IssuedToken, User

# AUTHORIZATION IS ONLY FOR TEST!!!
# DO NOT USE IT ON PRODUCTION


router = APIRouter(
    prefix="/users",
    tags=["USER"]
)


@router.post('',
            summary="Create a user",
            description="**Creates** a user for **authorization**",
            response_model=UserPublic,
            responses={
                422: {'model': CreateUser422}
            })
async def create_user_hand(data: CreatedUser):
    return data


@router.post('/login',
            summary="Logs in a user",
            description="**Logs in** a user for authentication and creates a refresh token",
            response_model=UserPublic,
            responses={
                400: {'model': LoginUser400},
                422: {'model': LoginUser422}
            })
async def login_user_hand(data: LoginUser):
    return data


@router.post('/token/{userId}',
            summary="Issues an access token",
            description="**Issues** an access token for being user authenticated",
            response_model=TokenPublic,
            responses={
                400: {'model': Token400},
                403: {'model': Token403},
                422: {'model': Token422}
            })
async def issue_access_token_hand(data: IssuedToken):
    return data


@router.get('/{id}',
            summary="Gets user",
            description="Gets all user info",
            response_model=UserPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': GetUser422}
            })
async def get_user_hand(data: User):
    return data
