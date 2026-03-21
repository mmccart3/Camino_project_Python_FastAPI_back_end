from fastapi import FastAPI
from .routers import health, add_item, get_data_api

app = FastAPI(
    title="Camino BE API",
    version="0.1.0",
)

# from db.db_connect import connect_to_db
# connect_to_db()

app.include_router(health.router)
app.include_router(add_item.router, prefix="/items", tags=["add_item"])
app.include_router(get_data_api.router, prefix="", tags=["get_data_api"])