import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User, Item
from app.auth import get_password_hash

# Database testing (SQLite in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    return TestClient(app)

@pytest.fixture(scope="function")
def test_user(db):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_admin(db):
    admin = User(
        username="adminuser",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpass123"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture(scope="function")
def user_token(client, test_user):
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    return response.json()["access_token"]

@pytest.fixture(scope="function")
def admin_token(client, test_admin):
    response = client.post("/auth/login", data={
        "username": "adminuser",
        "password": "adminpass123"
    })
    return response.json()["access_token"]