from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models.plan import Plan, CreatePlan, UpdatePlan
from db import SessionDep

router = APIRouter(tags=["Plans"])

@router.get("/plans", response_model=list[Plan], status_code=status.HTTP_200_OK)
async def get_plans(session: SessionDep):
    return session.exec(select(Plan)).all()


@router.post("/plans/create", response_model=Plan, status_code=status.HTTP_201_CREATED)
async def create_plan(plan_data: CreatePlan, session: SessionDep):
    newPlan = Plan.model_validate(plan_data.model_dump())
    session.add(newPlan)
    session.commit()
    session.refresh(newPlan)
    return newPlan