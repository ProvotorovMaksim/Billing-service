from fastapi import FastAPI as App

app = App()

@app.get("/")
async def read_route():
    return {"status": "running"}