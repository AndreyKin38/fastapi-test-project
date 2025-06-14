from fastapi import FastAPI

from app.ping import router as ping_router
from app.tasks.handlers import router as tasks_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router

app = FastAPI()

routers = [ping_router, tasks_router, auth_router, user_router]

for router in routers:
    app.include_router(router=router)



