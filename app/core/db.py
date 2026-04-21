from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_DB,MONGO_URI

client =AsyncIOMotorClient(MONGO_URI)
db=client[MONGO_DB]

def get_database():
    return db