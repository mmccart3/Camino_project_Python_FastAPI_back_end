from fastapi import FastAPI
from .routers import health, add_item, get_data_api

app = FastAPI(
    title="Camino BE API",
    version="0.1.0",
)


app.include_router(health.router)
app.include_router(get_data_api.router, prefix="", tags=["get_data_api"])
print("Included get_data_api router")
