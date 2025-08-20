from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
 

# DB_URL = "postgresql://postgres:pwd@localhost:5432/todo_db"
DB_URL = "sqlite:///./todosapp.db"

engine = create_engine(DB_URL,connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

