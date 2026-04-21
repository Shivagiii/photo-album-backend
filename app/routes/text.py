from fastapi import APIRouter
from app.core.db import db
from datetime import datetime


router = APIRouter(prefix="/test",tags=["Test"])

@router.get("/ping-db")
async def ping_db():
    collection = await db.list_collection_names()
    return {
        "message":"DB connected successfully",
        "collections":collection
    }

@router.post("/create-user")
async def create_user():
    user = {
        "name":"John Doe",
        "email":"sample@example.com",
        "created at":datetime.utcnow()
    }
    result = await db.users.insert_one(user)
    return {
        "message":"User created successfully",
        "user_id":str(result.inserted_id)
    }

@router.get("/users")
async  def get_users():
    users_curosor = db.users.find({})
    users=[]

    async for user in users_curosor:
        user["_id"]=str(user["_id"])
        users.append(user)
    
        
    return {"message":"Users fetched successfully",
            "count":len(users),
            "users": users} 
