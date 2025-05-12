from fastapi import FastAPI

app = FastAPI(title="LaSalsa API", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Welcome to LaSalsa API!"}