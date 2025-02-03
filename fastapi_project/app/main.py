import time
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_pagination import add_pagination
from db import create_all_tables
from .routers import customers, transactions, plans


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)
#app.include_router(invoices.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Middleware to print hedaers
@app.middleware("http")
async def print_headers(request: Request, call_next):
   response = await call_next(request)
   print(f"Request: {request.url} - Headers: {dict(response.headers)}")
   return response    

add_pagination(app)

security = HTTPBasic()

@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username == "robertbass" and credentials.password == "password":
        return {"message": f"Hello {credentials.username}"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")