from enum import Enum
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class PlanStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class CustomerPlan(SQLModel, table=True):
    plan_id: int = Field(default=None, foreign_key="plan.id", primary_key=True)
    customer_id: int = Field(default=None, foreign_key="customer.id", primary_key=True)
    status: PlanStatus = Field(default=PlanStatus.ACTIVE)

    
class PlanBase(SQLModel):
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)

class Plan(PlanBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customers: list["Customer"] = Relationship(back_populates="plans", link_model=CustomerPlan) # type: ignore


class CreatePlan(PlanBase):
    pass


class UpdatePlan(PlanBase):
    pass



