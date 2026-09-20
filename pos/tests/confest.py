import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from app.models import (
    category,
    customers,
    payments,
    products,
    receipts,
    sale_items,
    sales,
    suppliers,
    users,
)
from main import app


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@event.listens_for(test_engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def registered_user(client):
    payload = {
        "username": "test_cashier",
        "email": "cashier@example.com",
        "password": "Password123!",
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == 201
    return payload


@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post(
        "/users/login",
        json={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def category_record(client):
    response = client.post(
        "/categories/",
        json={"name": "Drinks", "description": "Hot and cold drinks"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def product_record(client, category_record):
    response = client.post(
        "/products",
        json={
            "name": "Coffee",
            "price": 3.50,
            "quantity": 20,
            "category_id": category_record["id"],
            "sku": "COFFEE-001",
        },
    )
    assert response.status_code == 201
    return response.json()
