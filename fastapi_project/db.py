import os
from pathlib import Path
from typing import Annotated
import environ
from fastapi import Depends
from sqlmodel import Session, create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

engine = create_engine(env.get("DATABASE_URL"))

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
