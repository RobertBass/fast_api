from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class TransactionBase(SQLModel):
    customer_id: int = Field(foreign_key="customer.id")
    amount: int = Field(default=None)
    description: str = Field(default=None)

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer: "Customer" = Relationship(back_populates="transactions") # type: ignore


class CreateTransaction(TransactionBase):
    pass
