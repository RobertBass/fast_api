import random
from sqlmodel import Session, select
from db import engine
from models.transaction import Transaction
from models.customer import Customer

def create_transactions():
    session = Session(engine)
    for x in range(100):
        Customer.id = random.randint(1, 2)
        session.add(
            Transaction(
                customer_id = Customer.id, 
                description=f"Transaction # { x + 1}",
                amount=random.randint(10, 500)
            )
        )
        print(f"Transaction {x + 1} added")
    session.commit()

create_transactions()