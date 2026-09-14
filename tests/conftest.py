import os
from typing import Generator
import pytest

# Sobrescribir la variable de entorno ANTES de importar módulos de app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator:
    """Fixture que provee una base de datos SQLite en memoria limpia por test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    """TestClient inyectando la sesión de BD SQLite aislada."""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(client) -> dict:
    """Fixture para registrar un usuario de prueba."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture(scope="function")
def user_token(client, test_user) -> str:
    """Fixture para autenticar usuario de prueba y devolver token JWT."""
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post(
        "/api/v1/auth/token",
        data={"username": login_data["username"], "password": login_data["password"]}
    )
    assert response.status_code == 200
    return response.json()["access_token"]