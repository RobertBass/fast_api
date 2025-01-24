from pydantic import BaseModel
from models.customer import Customer
from models.transaction import Transaction

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def total_amount(self):
        return sum([t.amount for t in self.transactions])