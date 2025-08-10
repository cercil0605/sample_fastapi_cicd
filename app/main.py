from fastapi import FastAPI
from app.api.routers import users

app = FastAPI(title="User Profile API")

@app.get("/health")
def health():
    return {"ok",True}

app.include_router(users.router)