from fastapi import FastAPI
from fastapi_pagination import add_pagination
from db import create_all_tables
from .routers import customers, transactions, plans


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)
#app.include_router(invoices.router)

add_pagination(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}