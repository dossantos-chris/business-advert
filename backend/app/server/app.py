from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from app.server.routes.business import router as BusinessRouter

#probably set up an origin list at some point
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#maybe add tags to this line and routes for documentation
app.include_router(BusinessRouter, prefix="/business")

