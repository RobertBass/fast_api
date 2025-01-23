import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from fastapi_project import db
from models.customer import CustomerInfo, CreateCustomer
from models.transaction import Transaction
from models.invoice import Invoice


app = FastAPI()


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


db_customers: list[CustomerInfo] = []

@app.get("/customers", response_model=list[CustomerInfo])
async def get_customers():
    return db_customers

@app.post("/customers/create", response_model=CustomerInfo, session=db.SessionDep)
async def create_customer(customer_data: CreateCustomer):
    customer = CustomerInfo.model_validate(customer_data.model_dump())
    db_customers.append(customer)
    customer.id = len(db_customers)
    return customer

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data