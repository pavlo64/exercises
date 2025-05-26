import pytest
from httpx import AsyncClient
from fastAPI.main.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

test_brand = {"id": 100, "name": "TestBrand"}
updated_brand = {"id": 100, "name": "TestBrandUpdated"}
existing_brand = {"id": 1, "name": "Nike"}


@pytest.mark.asyncio
async def test_get_all_brands(client):
    # Act
    response = await client.get("/brands")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert 1 in data
    assert data[1] == "Nike"


@pytest.mark.asyncio
async def test_create_brand(client):
    # Act
    response = await client.post("/brands", json=test_brand)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Brand added"
    assert data["brand"] == test_brand


@pytest.mark.asyncio
async def test_create_existing_brand(client):
    # Act
    response = await client.post("/brands", json=existing_brand)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Brand ID already exists"


@pytest.mark.asyncio
async def test_update_brand(client):
    # Arrange
    await client.post("/brands", json=test_brand)

    # Act
    response = await client.put("/brands", json=updated_brand)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Brand updated"
    assert data["brand"]["name"] == updated_brand["name"]


@pytest.mark.asyncio
async def test_delete_brand(client):
    # Arrange
    await client.post("/brands", json=test_brand)

    # Act
    response = await client.delete("/brands", json=test_brand)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Brand deleted"
    assert data["brand"] == test_brand
