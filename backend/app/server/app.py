from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.server.routes.business import router as BusinessRouter
from app.server.routes.user import router as UserRouter

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
app.include_router(BusinessRouter, tags = ["Business"], prefix = "/business")
app.include_router(UserRouter, tags = ["User"], prefix = "/user")

