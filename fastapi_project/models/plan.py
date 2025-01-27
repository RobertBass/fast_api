from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class CustomerPlan(SQLModel, table=True):
    plan_id: int = Field(default=None, foreign_key="plan.id", primary_key=True)
    customer_id: int = Field(default=None, foreign_key="customer.id", primary_key=True)

    
class Plan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    customers: list["Customer"] = Relationship(back_populates="plans", link_model=CustomerPlan) # type: ignore

