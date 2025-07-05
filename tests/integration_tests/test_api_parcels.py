import httpx
import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "name, weight, type_id, cost_usd",
    [
        ("Jacket", 544, 1, 200),
        ("Shirt", 50, 1, 10),
        ("Phone", 350, 2, 700),
        ("Pen", 1, 3, 5),
    ],
)
async def test_api_flow(
    name: str,
    weight: int,
    type_id: int,
    cost_usd: float,
    ac: AsyncClient,
):
    res_register = await ac.post(
        "/parcels",
        json={"name": name, "weight": weight, "type_id": type_id, "cost_usd": cost_usd},
    )
    assert ac.cookies.get("session_id")
    session_id = ac.cookies["session_id"]
    cookies = httpx.Cookies()
    cookies.set("session_id", session_id)
    register_data = res_register.json()
    assert res_register.status_code == 200
    assert "id" in register_data
    parcel_id = register_data["id"]
    res_parcel = await ac.get(f"/parcels/{parcel_id}", cookies=cookies)
    assert res_parcel.status_code == 200
    data_parcel = res_parcel.json()
    assert data_parcel["name"] == name
    assert data_parcel["cost_usd"] == cost_usd
    assert isinstance(data_parcel["type"], str)

    res_parcels = await ac.get("/parcels?limit=10&offset=0", cookies=cookies)
    assert res_parcels.status_code == 200
    data_parcel = res_parcels.json()
    assert len(data_parcel) == 1

    res_register2 = await ac.post(
        "/parcels",
        json={"name": name + "_second", "weight": weight, "type_id": type_id, "cost_usd": cost_usd},
        cookies=cookies,
    )
    assert res_register2.status_code == 200
    res_parcels2 = await ac.get("/parcels?limit=10&offset=0", cookies=cookies)
    assert res_parcels2.status_code == 200
    data_parcel2 = res_parcels2.json()
    assert len(data_parcel2) == 2


@pytest.mark.parametrize(
    "name, weight, type_id, cost_usd, status_code",
    [
        (11, 544, 1, 200, 422),
        (None, 50, 1, 10, 422),
        ("JoJo", 50, 1, -10, 422),
        ("Phone", -11, 2, 700, 422),
        ("Pen", 1, 113, 5, 404),
    ],
)
async def test_api_flow_invalid_input(
    name: str,
    weight: int,
    type_id: int,
    cost_usd: float,
    status_code: int,
    ac: AsyncClient,
):
    res_register = await ac.post(
        "/parcels",
        json={"name": name, "weight": weight, "type_id": type_id, "cost_usd": cost_usd},
    )
    print(res_register.text)
    assert res_register.status_code == status_code
