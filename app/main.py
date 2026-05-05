from fastapi import FastAPI
from app.module.auth import models as _auth_models
from app.module.task import models as _tasks_models
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(Bing=engine)


app = FastAPI()