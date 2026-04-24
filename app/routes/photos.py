from fastapi import APIRouter,HTTPException,Form,UploadFile,File
from datetime import datetime
from bson import ObjectId
from pathlib import Path
from app.core.db import db
import shutil
import uuid
router = APIRouter(prefix="/photos",tags=["photos"])

UPLOAD_DIR=Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/uploads")
async def upload_photos(
    event_id:str=Form(...),
    uploaded_by_user_id:str=Form(...),
    uploaded_by_name:str=Form(...),
    file:UploadFile = File(...)
):
    event = await  db.events.find_one({"_id":ObjectId(event_id)})
    if not event:
        return HTTPException(status_code=400,detail="Event not found")
    
    extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / unique_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"https://api.buildyourown.co.in/uploads/{unique_filename}"   

    photo_doc={
        "event_id":event_id,
        "uploaded_by_user_id":uploaded_by_user_id,
        "uploaded_by_name":uploaded_by_name,
        "image_url":image_url,
        "filename":unique_filename,
        "original_filename":file.filename,
        "uploaded_at":datetime.utcnow()
    }

    result = await db.photos.insert_one(photo_doc)

    photo_doc["_id"]=str(result.inserted_id)

    return{
        "message":"Uploaded succesfully",
        "photo":photo_doc
    }

@router.get("/event/{event_id}")
async def get_photos_by_event(event_id:str):

    photo_cursor = db.photos.find({"event_id":event_id}).sort("uploaded_at",-1)
    photos=[]

    async for photo in photo_cursor:
        photo["_id"]=str(photo["_id"])
        photos.append(photo)

    return{
        "message":"list",
        "photo_list":photos,
        "count":len(photos)
    }

@router.delete("/{photo_id}")
async def delete_photo(photo_id:str,user_id:str):

    photo = db.photos.find({"_id":ObjectId(photo_id)})

    if not photo:
        raise HTTPException(status_code=404,detail="Photo not found")
    
    if photo["uploaded_by_user_id"] != user_id:
        raise HTTPException(status_code=403,detail="Not allowed to delete this photo")
    
    await db.photos.delete_one({"_id":ObjectId(photo_id)})
 
    return {"message": "Photo deleted successfully"}
