from typing import Optional
from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship, Session, select
from models.plan import CustomerPlan
from db import engine

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        result = session.exec(select(Customer).where(Customer.email == value)).first()
        if result is not None:
            raise ValueError("Email already exists")
        return value


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer") # type: ignore
    plans: list["Plan"] = Relationship(back_populates="customers", link_model=CustomerPlan) # type: ignore
    

class CreateCustomer(CustomerBase):
    pass

class UpdateCustomer(CustomerBase):
    pass