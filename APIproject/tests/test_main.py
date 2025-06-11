import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from APIproject.main.main import app, brand_storage
from APIproject.main.models import Brand



brand_payload = {
    "name": "Reebok",
    "rate": 7,
    "catalogue": "Sportswear"
}
existing_brand_payload = {
    "name": "Nike",
    "rate": 7,
    "catalogue": "Sportswear"
}

@pytest.mark.asyncio
async def test_ping():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "API is working"}

async def test_get():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/brands")
    assert response.status_code == 200
    brands = response.json()
    assert isinstance(brands, list)
    for brand in brands:
        assert "brand_id" in brand and isinstance(brand["brand_id"], int)
        assert "name" in brand and isinstance(brand["name"], str)
        assert "rate" in brand and isinstance(brand["rate"], int | None)
        assert "catalogue" in brand and isinstance(brand["catalogue"], str | None)

async def test_direct_get():

    test_brand = Brand(brand_id=100, name="TestBrand", rate=9, catalogue="TestCategory")
    brand_storage.append(test_brand)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/brands/{test_brand.brand_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["brand_id"] == test_brand.brand_id
    assert data["name"] == test_brand.name
    assert data["rate"] == test_brand.rate
    assert data["catalogue"] == test_brand.catalogue

    brand_storage.remove(test_brand)

@pytest.mark.asyncio
async def test_get_nonexistent_brand():

    nonexistent_id = 9999
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/brands/{nonexistent_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Brand not found"}

@pytest.mark.asyncio
async def test_post():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        get_response1 = await ac.get("/brands")
        response = await ac.post("/brands", json=brand_payload)
        get_response2 = await ac.get("/brands")
    assert response.status_code == 200
    assert len(get_response1.json()) + 1 == len (get_response2.json())

@pytest.mark.asyncio
async def test_existing_brand_post():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        get_response1 = await ac.get("/brands")
        response = await ac.post("/brands", json=existing_brand_payload)
        get_response2 = await ac.get("/brands")
    assert response.status_code == 400
    assert response.json() == {"detail": "Brand with this name already exists"}
    assert len(get_response1.json()) == len (get_response2.json())

@pytest.mark.asyncio
async def test_patch():
    test_brand = Brand(brand_id=100, name="TestBrand", rate=9, catalogue="TestCategory")
    brand_storage.append(test_brand)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.patch(f"/brands/{test_brand.brand_id}", json=brand_payload)
        get_response = await ac.get(f"/brands/{test_brand.brand_id}")
    assert response.status_code == 200
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["brand_id"] == test_brand.brand_id
    assert data["name"] == brand_payload["name"]
    assert data["rate"] == brand_payload["rate"]
    assert data["catalogue"] == brand_payload["catalogue"]

    brand_storage[:] = [b for b in brand_storage if b.brand_id != test_brand.brand_id]

@pytest.mark.asyncio
async def test_patch_nonexistent_brand():
    nonexistent_id = 9999
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.patch(f"/brands/{nonexistent_id}", json=brand_payload)
    assert response.status_code == 404
    assert response.json() == {"detail": "Brand not found"}

@pytest.mark.asyncio
async def test_delete():
    test_brand = Brand(brand_id=100, name="TestBrand", rate=9, catalogue="TestCategory")
    brand_storage.append(test_brand)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        get_response1 = await ac.get("/brands")
        response = await ac.delete(f"/brands/{test_brand.brand_id}")
        get_response2 = await ac.get("/brands")
    assert response.status_code == 200
    assert len(get_response1.json()) -1 == len(get_response2.json())

@pytest.mark.asyncio
async def test_delete_nonexistent_brand():
    nonexistent_id = 9999
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete(f"/brands/{nonexistent_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Brand not found"}


