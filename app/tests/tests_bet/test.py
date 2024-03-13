from httpx import AsyncClient
import json
import pytest


async def test_get_actual_events(ac_bet:AsyncClient):
    response = await ac_bet.get('/actual_events')
    data = json.loads(response.text)
    assert len(data) ==1
    assert response.status_code == 200


async def test_get_bets(ac_bet:AsyncClient):
    response = await ac_bet.get('/history_bets')
    data = json.loads(response.text)
    assert len(data) ==2
    assert response.status_code == 200


@pytest.mark.parametrize("event_id, amount, status_code, message", [
    (1, 100, 200, {'message': 'Bet successfully created'}),
    (3, 100, 404, {'detail': 'Event not found'}),
    (1,300,200, {'message': 'Bet successfully created'}),
    (1,109.0909,422,{"detail":"Request validation failed"})
])
async def test_create_bet(event_id,amount,status_code,message,ac_bet:AsyncClient):
    response = await ac_bet.post('/create_bet', json={"event_id":event_id, "amount":amount})
    assert response.status_code == status_code
    if status_code==200:
        assert response.json() == message