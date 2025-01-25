from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from models.customer import Customer

class TransactionBase(SQLModel):
    amount: int = Field(default=None)
    description: str = Field(default=None)

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")


class CreateTransaction(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")