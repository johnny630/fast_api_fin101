from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/ping")
async def ping():
  return {"message": "pong"}

@app.get("/time")
async def time():
  return {"time": datetime.now().isoformat()}
