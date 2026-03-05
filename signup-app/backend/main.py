from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {}

class User(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    users[user.username] = user.password
    return {"message": "User created successfully"}

@app.post("/signin")
def signin(user: User):
    if user.username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "Login successful"}