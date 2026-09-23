from fastapi import FastAPI

app = FastAPI(title="SecureVault API")


@app.get("/health")
def health_check():
    return {"status": "ok"}