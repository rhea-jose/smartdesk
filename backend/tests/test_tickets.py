import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

engine=create_engine(
    "sqlite://",
    connect_args={"check_same_thread":False},
    poolclass=StaticPool
    # keeps one shared in-memory DB across connections
)

TestingSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def override_get_db():
    db=TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db]=override_get_db

client= TestClient(app)
@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_health():
    assert client.get("/health").json()=={"status":"ok"}

def test_create_and_get_ticket():
    r=client.post(
        "/tickets",
        json={
            "title":"Cannot log in",
            "description":"Password reset failed"
        }
    )
    assert r.status_code==201
    body=r.json()
    assert body["status"]=="open"
    assert client.get(f"/tickets/{body['id']}").status_code==200

def test_validation_rejects_short_title():
    r=client.post(
        "/tickets",
        json={
            "title":"a",
            "description":"long enough text"
        }
    )
    assert r.status_code == 422
    # 422 means request data itself failed validation

def test_update_status():
    tid=client.post(
        "/tickets",
        json={
            "title":"Bill issue",
            "description":"Charged twice"
        }
    ).json()['id']

    r=client.patch(
        f"/tickets/{tid}",
        json={
            "status":"resolved"
        }
    )

    assert r.json()['status']=='resolved'

def test_invalid_status_rejected():
    tid=client.post(
        "/tickets",
        json={
            "title":"Bill issue",
            "description":"Charged twice"
        }
    ).json()['id']

    assert client.patch(
        f"/tickets/{tid}",
        json={
            "status":"banana"
        }
    ).status_code==422

def test_get_missing_ticket_404():
    assert client.get("/tickets/999").status_code == 404

def test_filter_by_status():
    client.post(
        "/tickets",
        json={
            "title": "Ticket one",
            "description": "first ticket"
        }
    )
    tid = client.post(
        "/tickets",
        json={
            "title": "Ticket two",
            "description": "second ticket"
        }
    ).json()["id"]

    client.patch(
        f"/tickets/{tid}",
        json={"status": "resolved"}
    )

    r=client.get(
        "/tickets",
        params={"status":"resolved"}
    )

    assert len(r.json()) == 1
    

