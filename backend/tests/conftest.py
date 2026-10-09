import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.main import app
from backend.app.db.base import Base
from backend.app.db.session import get_db
from backend.app.core.security import get_password_hash
from backend.app.models.user import User

# In-memory SQLite for automated tests
TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine_test)
    # Seed authority users into test DB
    db = TestingSessionLocal()
    users = [
        User(
            name="Admin User",
            email="admin@test.edu",
            password_hash=get_password_hash("TestPass123!"),
            role="administrator"
        ),
        User(
            name="HOD User",
            email="hod@test.edu",
            password_hash=get_password_hash("TestPass123!"),
            role="hod",
            department="CSE"
        ),
        User(
            name="Dean User",
            email="dean@test.edu",
            password_hash=get_password_hash("TestPass123!"),
            role="dean",
            department="Student Affairs"
        ),
        User(
            name="Higher Auth User",
            email="director@test.edu",
            password_hash=get_password_hash("TestPass123!"),
            role="higher_authority"
        ),
        User(
            name="Student User",
            email="student@test.edu",
            password_hash=get_password_hash("TestPass123!"),
            role="student"
        ),
    ]
    db.add_all(users)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
