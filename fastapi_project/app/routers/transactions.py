from fastapi import APIRouter, Query, status, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import select
from models.customer import Customer
from models.transaction import Transaction, CreateTransaction
from db import SessionDep

router = APIRouter(tags=["Transactions"])


@router.post("/transactions", status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: CreateTransaction, session: SessionDep):
    transaction_info = transaction_data.model_dump()
    customer = session.get(Customer, transaction_info.get("customer_id"))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    transaction = Transaction.model_validate(transaction_info)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("/transactions", status_code=status.HTTP_200_OK)
async def get_transactions(session: SessionDep) -> Page[Transaction]:
    return paginate(session, select(Transaction))

