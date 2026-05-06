from fastapi import FastAPI
from app.module.auth import models as _auth_models
from app.module.auth.router import router as auth_router
from app.module.task import models as _tasks_models
from app.module.task.router import router as tasks_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(tasks_router,prefix='/tasks' ,tags=['tasks'])