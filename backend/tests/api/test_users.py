import pytest
from httpx import AsyncClient

import tests.api.constants as const
from tests.api.utils.assertion import assert_json_response
from src.schemas.user import UserPublic, CreateUser422


@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_create_user_hand(client: AsyncClient):
    uri = "/users"
    response = await client.post(uri, json=const.VALID_USER_PAYLOAD)
    assert_json_response(response, 200, UserPublic)
    response = await client.post(uri, json=const.VALID_USER_PAYLOAD)
    assert_json_response(response, 422, CreateUser422)
    response = await client.post(uri, json=const.INVALID_USER_PAYLOAD)
    assert_json_response(response, 422, CreateUser422)


@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_login_user_hand(client: AsyncClient):
    uri = "/login"
    

@pytest.mark.asyncio
@pytest.mark.order(3)
async def test_issue_access_token_hand(client: AsyncClient):
    uri = ""


@pytest.mark.asyncio
@pytest.mark.order(4)
async def test_get_user_hand(client: AsyncClient):
    uri = ""   
