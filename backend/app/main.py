import os

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.files import router as files_router

from fastapi.middleware.cors import CORSMiddleware

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173"
    ).split(",")
    if origin.strip()
]

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(files_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)