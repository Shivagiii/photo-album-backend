from fastapi import APIRouter,HTTPException
from app.core.db import db
from datetime import datetime

router = APIRouter(prefix="/events",tags=["Events"])

DEFAULT_EVENTS = [
    {"name": "Haldi", "slug": "haldi", "sort_order": 1},
    {"name": "Mehendi", "slug": "mehendi", "sort_order": 2},
    {"name": "Sangeet", "slug": "sangeet", "sort_order": 3},
    {"name": "Mandwa", "slug": "mandwa", "sort_order": 4},
    {"name": "Shaadi", "slug": "shaadi", "sort_order": 5},
    {"name": "Reception", "slug": "reception", "sort_order": 6},
]


@router.post("/seed")
async def seed_events():
    inserted=0

    for event in DEFAULT_EVENTS:
        existing = await db.events.find_one({"slug":event["slug"]})
        if not existing:
            await db.events.insert_one({
                **event,
                "created at":datetime.utcnow()
            })
            inserted+=1

    return {
        "message":"Events added",
        "inserted_count":inserted
    }

@router.get("")
async def get_events():

    events_cursor =  db.events.find({})
    if not events_cursor:
        return HTTPException(status_code=400,detail="No events found")
    
    events=[]

    async for event in events_cursor:
        event["_id"]=str(event["_id"])
        events.append(event)



    return {
        "message":"Event list fetched successfully",
        "event_list":events,
        "count":len(events)
    }