from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel

class CustomerInfo(SQLModel, table=True):
    id: int
    name: str
    description: str | None = None
    email: EmailStr
    age: int

class CreateCustomer(BaseModel):
    name: str
    description: str | None
    email: EmailStr
    age: int
