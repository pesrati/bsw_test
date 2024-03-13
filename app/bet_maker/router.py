import time

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, status

from app.bet_maker.dao import BetsDAO
from app.bet_maker.schemas import SBets
from app.line_provider.dao import EventsDAO

app = FastAPI(
    title="Bet Maker Service", version="1.0", description="This is a bet maker service"
)


@app.get("/actual_events")
async def get_actual_events() -> list:
    """
    Retrieves a list of events that are currently being played.

    Returns:
        list: A list of events that are currently being played.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/events")
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get events from line_provider service",
        )
    data = response.json()
    print(data, time.time())
    events = (x for x in data if x["deadline"] > time.time())
    return events


@app.post("/create_bet")
async def create_bet(bet_data: SBets) -> dict:
    """
    Create a new bet.

    Args:
        bet_data (SBets): The data for the new bet.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the event specified in the bet data is not found.
    """
    existing_event = await EventsDAO.find_one_or_none(id=bet_data.event_id)
    if existing_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    await BetsDAO.add(**bet_data.model_dump())
    return {"message": "Bet successfully created"}


@app.get("/history_bets")
async def get_bets() -> list:
    """
    Retrieve a list of bets joined with events.

    Returns:
        list: A list of bets joined with events.
    """
    return await BetsDAO.join_bets_with_events()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
