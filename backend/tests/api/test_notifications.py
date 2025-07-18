import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.order(5)
async def test_get_notifications_hand(client: AsyncClient):
    uri = ""


@pytest.mark.asyncio
@pytest.mark.order(6)
async def test_create_notification_hand(client: AsyncClient):
    uri = ""  
