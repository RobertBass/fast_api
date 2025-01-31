from fastapi import APIRouter, HTTPException, Query, status
from db import SessionDep
from sqlmodel import select
from models.plan import Plan, CustomerPlan, PlanStatus
from models.customer import Customer, CreateCustomer, UpdateCustomer

router = APIRouter(tags=["Customers"])
db_customers: list[Customer] = []

@router.get("/customers", status_code=status.HTTP_200_OK)
async def get_customers(session:SessionDep):
    customers = session.exec(select(Customer)).all()
    customers_with_plans = []
    for customer in customers:
        # Carga de los planes del cliente
        customerplans = session.exec(select(Plan).where(CustomerPlan.customer_id == customer.id)).all()
        customers_with_plans.append({
            "Customer": customer,
            "Plans": customerplans
        })
    return customers_with_plans


@router.get("/customers/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customer(customer_id: int, session:SessionDep):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_plans = session.exec(select(Plan).where(CustomerPlan.customer_id == customer_id)).all()
    response = {
        "customer": customer,
        "plans": customer_plans
    }
    return response


@router.post("/customers/create", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CreateCustomer, session:SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.patch("/customers/update/{customer_id}", response_model=Customer, status_code=status.HTTP_202_ACCEPTED)
async def update_customer(customer_id: int, customer_data: UpdateCustomer , session:SessionDep):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    customer_info = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_info)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.delete("/customers/delete/{customer_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_customer(customer_id: int, session:SessionDep):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {
        "message": "Customer deleted",
        "customer": customer.model_dump()
    }


@router.post("/customers/addplan/{customer_id}/{plan_id}", status_code=status.HTTP_201_CREATED)
async def add_customer_to_plan(customer_id: int, plan_id: int, session:SessionDep, plan_status: PlanStatus = Query()):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    plan = session.get(Plan, plan_id)
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
    customer_plan = CustomerPlan(plan_id=plan.id, customer_id=customer.id, status=plan_status)
    session.add(customer_plan)
    session.commit()
    session.refresh(customer_plan)
    return customer_plan



@router.get("/customers/{customer_id}/plans", status_code=status.HTTP_200_OK)
async def get_customer_plans(customer_id: int, session:SessionDep, plan_status: PlanStatus = Query()):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    plans = session.exec(select(CustomerPlan).where(CustomerPlan.customer_id == customer_id, CustomerPlan.status == plan_status)).all()
    return plans