from typing import Callable, Awaitable, Type, Annotated

from fastapi import Depends, HTTPException, status, Response, Path, Header

from src.utils.service import Service
from src.types.dependency_factory import TSchemaBody, TSchemaPublic


class DependencyFactory:
    def __init__(
        self,
        service_dep: Callable[[], Awaitable[Service]],
        SchemaBody: Type[TSchemaBody],
        SchemaPublic: Type[TSchemaPublic]
    ):
        self.service_dep = service_dep
        self.SchemaBody = SchemaBody
        self.SchemaPublic = SchemaPublic
        
    def token_dep(self) -> Callable[[], Awaitable[str]]:
        async def dep(
            service = Depends(self.service_dep),
            authorization: str | None = Header(None)):
            print("AUTH", authorization)
            try:
                h, token = authorization.split(' ')
                if h.lower() != 'bearer':
                    raise ValueError
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"   
                )
            data = await service.validate_token(token)
            if isinstance(id, str):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=data
                )
            return token
        return dep
        
    def create_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        SchemaBody = self.SchemaBody
        async def dep(
            body: SchemaBody,
            service: Service = Depends(self.service_dep)
            ) -> TSchemaPublic:
            data = await service.create(body)
            if isinstance(data, str):
                raise HTTPException(
                    detail=data,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            response = self.SchemaPublic(**body.model_dump(), id=data)
            return response
        return dep
    
    def get_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        async def dep(
            service = Depends(self.service_dep),
            id: int = Path(..., examples=[1])):
            data = await service.get(id)
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Id has not found"
                )
            response = self.SchemaPublic.model_validate(data, from_attributes=True)
            return response
        return dep
    
    def set_cookie(
        self,
        response: Response,
        key: str,
        value: str,
        max_age: int) -> None:
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=max_age
        )
