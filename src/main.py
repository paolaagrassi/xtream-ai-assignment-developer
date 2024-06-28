from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.diamond_router import router as diamond_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diamond_router)


