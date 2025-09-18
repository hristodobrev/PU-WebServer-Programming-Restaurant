from fastapi import FastAPI
from routers import table_router, product_router, order_router

app = FastAPI()

app.include_router(table_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)