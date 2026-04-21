import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def override():
        yield session

    app.dependency_overrides[get_session] = override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_message(client):
    response = client.post("/messages", json={
        "name": "Ada",
        "email": "ada@test.com",
        "subject": "Hello",
        "message": "Testing 123",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ada"
    assert data["email"] == "ada@test.com"
    assert "id" in data
    assert "created_at" in data


def test_list_messages(client):
    client.post("/messages", json={
        "name": "Bob",
        "email": "bob@test.com",
        "subject": "Hi",
        "message": "First",
    })
    client.post("/messages", json={
        "name": "Clara",
        "email": "clara@test.com",
        "subject": "Hey",
        "message": "Second",
    })
    response = client.get("/messages")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_message_not_found(client):
    response = client.get("/messages/999")
    assert response.status_code == 404


def test_delete_message(client):
    create = client.post("/messages", json={
        "name": "Del",
        "email": "del@test.com",
        "subject": "Bye",
        "message": "Delete me",
    })
    msg_id = create.json()["id"]
    response = client.delete(f"/messages/{msg_id}")
    assert response.status_code == 200
    assert client.get(f"/messages/{msg_id}").status_code == 404
