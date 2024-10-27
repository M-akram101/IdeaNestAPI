from fastapi import FastAPI

import routes.auth as auth
from database import init
from routes import organizations
app = FastAPI()

@app.on_event('startup')
async def connect():
    await init()


app.include_router(organizations.router, prefix = "/organizations", tags= ['Organizations'])
app.include_router(auth.router, prefix = "", tags= ['Authentication'])



