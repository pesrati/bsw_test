import pytest 
from httpx import AsyncClient

async def test_get_events(ac_line: AsyncClient):
    response = await ac_line.get("/events")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2

async def test_get_event(ac_line: AsyncClient):
    response = await ac_line.get(f'/event/1')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['coefficient'] == 1.14
    assert data['state'] == 'N'

async def test_get_event_not_found(ac_line: AsyncClient):
    response = await ac_line.get(f'/event/3')
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Event not found'

async def test_update_test(ac_line: AsyncClient):
    response = await ac_line.patch("/event/update/{event_id}?id=1&state=N",data = {"id":1, "state": 'N'})
    print(response.text)
    assert response.status_code == 200

async def test_update_test_failed(ac_line: AsyncClient):
    response = await ac_line.patch("/event/update/{event_id}?id=3&state=W",data = {"id":3, "state": 'W'})
    print(response.text)
    assert response.status_code == 404
    
@pytest.mark.parametrize("id, coefficient, deadline, state, status_code", [
    (1,1.14, 1612137600, 'N', 409),
    (2,3.15, 1612137600, 'N', 409),
    (3,1.98, 1000,'N', 200),
])
async def test_create_event(id, coefficient, deadline, state, status_code, ac_line: AsyncClient):
    response = await ac_line.put('/event',json = {
        'id': id,
        'coefficient': coefficient,
        'deadline': deadline,
        'state': state
    })
    assert response.status_code == status_code
