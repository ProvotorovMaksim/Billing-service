from fastapi import FastAPI as App
from payments import router as payments_router
from tariffs import router as tariff_router
from subscriptions import router as subscriptions_router

app = App()

app.include_router(payments_router)
app.include_router(tariff_router)
app.include_router(subscriptions_router)

@app.get("/")
async def read_route():
    return {"status": "running"}
