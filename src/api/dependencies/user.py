from typing import Annotated, Callable, Awaitable, Optional

from fastapi import Depends, HTTPException, status, Cookie, Response, Path

from src.utils.dependency_factory import DependencyFactory
from src.api.dependencies.db import DBSession
from src.repositories import UserRepository
from src.services import UserService
from src.schemas.user import UserBody, UserPublic, TokenPublic
from src.enums.user import TokenEnum


async def service_dep(session: DBSession) -> UserService:
    return UserService(session, UserRepository)


class UserDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=UserBody,
            SchemaPublic=UserPublic
        )
        
    def login_user_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        async def dep(
            body: UserBody,
            response: Response,
            service: UserService = Depends(self.service_dep),
            refreshToken: Optional[str] = Cookie(None, examples=[None])) -> UserPublic:
            if refreshToken:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is already authenticated. Refresh token has found"
                )
            data = await service.login(body)
            if isinstance(data, str):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=data
                )
            self.set_cookie(response, "refreshToken", data.get("tokenId"), TokenEnum.REFRESH_TOKEN_EXP.value)
            return UserPublic(**data)
        return dep
    
    def issue_access_token_dep(self) -> Callable[[], Awaitable[TokenPublic]]:
        async def dep(
            response: Response,
            service: UserService = Depends(self.service_dep),
            refreshToken: Optional[str] = Cookie(None, examples=[None]),
            userId: int = Path(..., examples=[1])) -> TokenPublic:
            if not refreshToken:
                raise HTTPException(
                    status_code=status.HTTP_403_UNAUTHORIZED,
                    detail="User is not authenticated. Refresh token has not found"
                )
            data = await service.issue_token(refreshToken, userId)
            if isinstance(data, tuple):
                raise HTTPException(
                    status_code=data[1],
                    detail=data[0]
                )
            self.set_cookie(response, "refreshToken", data.get("tokenId"), data.get("exp"))
            return TokenPublic(accessToken=data.get("accessToken"))
        return dep
    
    def get_user_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        async def dep(
            service: UserService = Depends(self.service_dep),
            token: str = Depends(self.token_dep()),
            id: int = Path(..., examples=[1])):
            data = await service.get(id)
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Id has not found"
                )
            response = UserPublic.model_validate(data, from_attributes=True)
            return response
        return dep
        

dependencies = UserDependencyFactory()


CreatedUser = Annotated[UserPublic, Depends(dependencies.create_dep())]

LoginUser = Annotated[UserPublic, Depends(dependencies.login_user_dep())]

IssuedToken = Annotated[TokenPublic, Depends(dependencies.issue_access_token_dep())]

User = Annotated[UserPublic, Depends(dependencies.get_user_dep())]
