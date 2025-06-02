from fastapi import FastAPI
from handlers import ping_router, tasks_router, user_router, auth_router

app = FastAPI()

for router in [tasks_router, ping_router, user_router, auth_router]:
    app.include_router(router=router)



