from fastapi import FastAPI

from app.server.routes.business import router as BusinessRouter

app = FastAPI()
#maybe add tags to this line and routes for documentation
app.include_router(BusinessRouter, prefix="/business")