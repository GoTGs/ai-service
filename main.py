from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import recommendation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommendation.router)