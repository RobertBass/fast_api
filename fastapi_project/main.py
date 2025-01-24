import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from db import SessionDep, create_all_tables
from models.customer import Customer, CreateCustomer
from models.transaction import Transaction
from models.invoice import Invoice
from sqlmodel import select


app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return {"message": "Hello World"}

country_timezones = {
    "US": "America/New_York",
    "UK": "Europe/London",
    "DE": "Europe/Berlin",
    "FR": "Europe/Paris",
    "EC": "America/Guayaquil",
    "JP": "Asia/Tokyo",
    "CN": "Asia/Shanghai",
    "IN": "Asia/Kolkata",
    "CO": "America/Bogota",
    "BR": "America/Sao_Paulo",
    "MX": "America/Mexico_City",
}

@app.get("/date/{iso_code}")
async def date(iso_code: str):
    iso = iso_code.upper()
    timezone = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone)
    return {
        "City": timezone, 
        "Date": datetime.now(tz).isoformat()
        }


#db_customers: list[CustomerInfo] = []

@app.get("/customers", response_model=Customer)
async def get_customers(session=SessionDep):
    return session.execute(select(Customer)).all()


@app.post("/customers/create", response_model=Customer)
async def create_customer(customer_data: CreateCustomer, session=SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    #db_customers.append(customer)
    #customer.id = len(db_customers)
    return customer

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data