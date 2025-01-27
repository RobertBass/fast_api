from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from models.plan import CustomerPlan

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer") # type: ignore
    plans: list["Plan"] = Relationship(back_populates="customers", link_model=CustomerPlan) # type: ignore
    

class CreateCustomer(CustomerBase):
    pass

class UpdateCustomer(CustomerBase):
    pass