from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field

class Customer(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

class CreateCustomer(BaseModel):
    name: str
    description: str | None
    email: EmailStr
    age: int
