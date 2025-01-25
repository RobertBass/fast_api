from fastapi import APIRouter, HTTPException, status
from db import SessionDep
from sqlmodel import select
from models.customer import Customer, CreateCustomer, UpdateCustomer

router = APIRouter(tags=["Customers"])
db_customers: list[Customer] = []

@router.get("/customers", response_model=list[Customer], status_code=status.HTTP_200_OK)
async def get_customers(session:SessionDep):
    return session.exec(select(Customer)).all()


@router.get("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def get_customer(customer_id: int, session:SessionDep):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.post("/customers/create", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CreateCustomer, session:SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.patch("/customers/update/{customer_id}", response_model=Customer, status_code=status.HTTP_202_ACCEPTED)
async def update_customer(customer_id: int, customer_data: UpdateCustomer , session:SessionDep):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    customer_info = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_info)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.delete("/customers/delete/{customer_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_customer(customer_id: int, session:SessionDep):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {
        "message": "Customer deleted",
        "customer": customer.model_dump()
    }