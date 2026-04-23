from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,EmailStr
from app.utils.otp import generate_otp
from datetime import datetime,timedelta
from app.core.db import db

router = APIRouter(prefix="/auth",tags=['AUTH'])

class RequestLoginSchema(BaseModel):
    email:EmailStr
    
class VerifyOtpSchema(BaseModel):
    email:EmailStr
    otp:str 

@router.post("/request-login")
async def request_login(payload:RequestLoginSchema):
    email = payload.email.strip().lower()
    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    await db.login_tokens.update_many(
        {"email":email,"used":False},
        {"$set":{"used":True}})

    await db.login_tokens.insert_one({
        "email":email,
        "otp":otp,
        "expires_at":expires_at,
        "used":False,
        "created at":datetime.utcnow()
    })

    return {
        "message":"OTP generated!",
        "email":email,
        "otp":otp,
        "expires_at":expires_at
    }


@router.post("/verify-otp")
async def verify_otp(payload:VerifyOtpSchema) :
    email=payload.email.strip().lower()
    otp=payload.otp.strip()

    response = await db.login_tokens.find_one(
        {"email":email,"used":False,"otp":otp},
        sort=[("created at",-1)]
        )
    
    if not response:
        raise HTTPException(status_code=400, detail="Invaild OTP")
    
    if response["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=400,detail="OTP expired")
    
    await db.login_tokens.update_one(
        {"_id":response["_id"]},
        {"$set":{"used":True}}
    )

    user = await db.users.find_one({"email":email})

    if not user:
       result= await db.users.insert_one({
           "email":email,
           "name":email.split("@")[0],
           "created at":datetime.utcnow()
        })
       user = await db.users.find_one({"_id":result.inserted_id})

    user["_id"] = str(user["_id"])

    return{
        "message":"Vertified successfully",
        "user":user
    }
       