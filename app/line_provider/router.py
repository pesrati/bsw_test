import time

import uvicorn
from fastapi import FastAPI, HTTPException,  status

from app.line_provider.dao import EventsDAO
from app.line_provider.schemas import SEvent

app = FastAPI(
    title="Line Provider Service",
    version="1.0",
    description="This is a line provider service",
)


@app.put("/event")
async def create_event(event_data: SEvent) -> dict:
    """
    Create a new event.

    Args:
        event_data (SEvent): The event data.

    Returns:
        dict: A dictionary containing the message indicating the success of the event creation.
    """
    existing_event = await EventsDAO.find_one_or_none(id=event_data.id)
    if existing_event:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Event already exists"
        )
    event_data.deadline += time.time()
    await EventsDAO.add(**event_data.model_dump())
    return {"message": "Event successfully created"}


@app.get("/event/{event_id}")
async def get_event(event_id: int):
    """
    Retrieve an event by its ID.

    Args:
        event_id (int): The ID of the event to retrieve.

    Returns:
        dict: The event information.

    Raises:
        HTTPException: If the event is not found.
    """
    existing_event = await EventsDAO.find_one_or_none(id=event_id)
    if not existing_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return existing_event


@app.get("/events")
async def get_events() -> list[SEvent]:
    """
    Retrieve a list of events.

    Returns:
        A list of SEvent objects representing the events.
    """
    return await EventsDAO.find_all()


@app.patch("/event/update/{event_id}")
async def update_event(id: int, state: str) -> dict:
    """
    Update the status of an event.

    Args:
        event_id (int): The ID of the event to be updated.
        status (str): The new status of the event. Possible values are 'W' (WIN), 'L' (LOSE), or 'N' (Not finished).

    Returns:
        dict: A dictionary containing a message indicating the success of the update.

    Raises:
        HTTPException: If the event with the specified ID is not found.
    """
    existing_event = await EventsDAO.find_one_or_none(id=id)
    if  existing_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    await EventsDAO.update(id=id, state=state)
    return {"message": "Event successfully updated"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
