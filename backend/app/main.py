from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.files import router as files_router


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(files_router)