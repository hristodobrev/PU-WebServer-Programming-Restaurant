from fastapi import FastAPI
from routers import tables

app = FastAPI()

app.include_router(tables.router)