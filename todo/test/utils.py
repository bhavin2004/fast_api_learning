from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
import pytest
from ..router.user import bcrypt_contest
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from todo.main import app
from ..models import Base
from ..models import Todo,Users





DB_URL = "postgresql://postgres:pwd@localhost:5432/test_todo_db"

engine = create_engine(DB_URL,poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine) 

Base.metadata.create_all(bind=engine)

def overide_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()

def overide_current_user():
    return {'username': 'codingwithrobytest', 'id': 1, 'role': 'admin'}


client = TestClient(app)


@pytest.fixture
def test_data():
    try:
        user = Users(
        username="codingwithrobytest",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_contest.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111"
    )
        db = TestingSessionLocal()
        db.add(user)
        db.commit()
        
        todo = Todo(
            title="Learn to code!",
            description="Need to learn everyday!",
            priority=5,
            complete=False,
            owner_id=1,
        )

        db = TestingSessionLocal()
        db.add(todo)
        db.commit()
        yield todo
    finally:
        with engine.connect() as connection:
            # connection.execute(text("DELETE FROM todos;"))
            # connection.execute(text("truncate table users;"))
            connection.execute(text("TRUNCATE TABLE users, todos RESTART IDENTITY CASCADE;"))
            connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username="codingwithrobytest",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_contest.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        # connection.execute(text("DELETE FROM users;"))
        connection.execute(text("TRUNCATE TABLE users, todos RESTART IDENTITY CASCADE;"))
        connection.commit()