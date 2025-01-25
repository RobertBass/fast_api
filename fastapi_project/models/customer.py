from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from models.transaction import Transaction


class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    

class CreateCustomer(CustomerBase):
    pass

class UpdateCustomer(CustomerBase):
    pass