from httpx import AsyncClient


async def test_api_flow(
    ac: AsyncClient,
):
    res = await ac.get("/parcel_types")
    assert res.status_code == 200
    data_types = res.json()
    assert len(data_types) == 3
