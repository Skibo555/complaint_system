import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import database
from resources.routes import api_router


ORIGINS = [
    "http://localhost",
    "http://localhost:8000"
]


app = FastAPI()
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_orings=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def start_up():
    await database.connect()


@app.on_event("shutdown")
async def shut_down():
    await database.disconnect()


@app.get("/", status_code=200)
async def home():
    return {
        "message": "You are wellcome."
    }


@app.post("/hello/{name}", status_code=200)
async def hello(name):
    return {
        "Greetings": f"Hello, {name}!"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
