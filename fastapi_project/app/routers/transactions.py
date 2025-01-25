from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models.customer import Customer
from models.transaction import Transaction
from db import SessionDep

router = APIRouter(tags=["Transactions"])


@router.post("/transactions")
async def create_transaction(transaction_data: Transaction, session: SessionDep):
    transaction_info = transaction_data.model_dump()
    customer = session.get(Customer, transaction_info.get["customer_id"])
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    transaction = Transaction.model_validate(transaction_info)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("/transactions")
async def get_transactions(transaction_data: create_transaction, session: SessionDep):
    return session.exec(select(Transaction)).all()
