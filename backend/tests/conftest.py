
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.db import models
from app.services.storage.local import LocalStorage
import app.api.files as files_api


@pytest.fixture
def client(tmp_path, monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    test_storage = LocalStorage(
        base_path=str(tmp_path / "storage")
    )
    monkeypatch.setattr(files_api, "storage", test_storage)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def create_user(client):
    def _create_user():
        unique = uuid.uuid4().hex[:12]

        payload = {
            "login": f"user_{unique}",
            "email": f"{unique}@example.com",
            "password": "StrongTestPassword123!",
        }

        register_response = client.post(
            "/auth/register",
            json=payload,
        )

        assert register_response.status_code == 200

        login_response = client.post(
            "/auth/login",
            json={
                "email": payload["email"],
                "password": payload["password"],
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        return {
            "payload": payload,
            "token": token,
            "headers": {
                "Authorization": f"Bearer {token}"
            },
        }

    return _create_user