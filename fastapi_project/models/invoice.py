'''from typing import Optional
from sqlmodel import SQLModel, Field
from models.customer import Customer
from models.transaction import Transaction

class InvoiceBase(SQLModel):
    customer: Customer
    transactions: list[Transaction]
    total: int = Field(default=None)

    @property
    def total_amount(self):
        return sum([t.amount for t in self.transactions])
    

class Invoice(InvoiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)'''