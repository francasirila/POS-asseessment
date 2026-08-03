import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from pos.core.rate_limit import limiter
import pos.models

from pos.routers.auth import router as auth_router
from pos.routers.users import router as users_router
from pos.routers.categories import router as categories_router
from pos.routers.suppliers import router as suppliers_router
from pos.routers.products import router as products_router
from pos.routers.customers import router as customers_router
from pos.routers.sales import router as sales_router

pos_api = FastAPI(title="Boutique POS API")

pos_api.state.limiter = limiter

_origins_env = os.getenv("ALLOWED_ORIGINS")
ALLOWED_ORIGINS = _origins_env.split(",") if _origins_env else ["http://localhost:3000"]

pos_api.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

pos_api.include_router(auth_router)
pos_api.include_router(users_router)
pos_api.include_router(categories_router)
pos_api.include_router(suppliers_router)
pos_api.include_router(products_router)
pos_api.include_router(customers_router)
pos_api.include_router(sales_router)


@pos_api.on_event("startup")
def create_tables() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        print(f"Warning: could not create database tables: {exc}")