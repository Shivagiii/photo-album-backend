from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.text import router as text_router
from app.routes.auth import router as auth_router
from app.routes.events import router as event_router
from app.routes.photos import router as photo_router

app= FastAPI()
origins = [
    "https://buildyourown.co.in",
    "https://www.buildyourown.co.in",
    "http://localhost:3001",
    "http://localhost:3000",
    "http://127.0.0.1:3001",
  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.include_router(text_router)
app.include_router(auth_router)
app.include_router(event_router)
app.include_router(photo_router)



@app.get("/")
async def root():
    return {"message": "Backend is running 🚀"}