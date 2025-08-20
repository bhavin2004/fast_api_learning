from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,CheckConstraint,ForeignKey

class Todo(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer,CheckConstraint("priority BETWEEN 1 AND 5"))
    complete = Column(Boolean,default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    
class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
    role = Column(String)
    phone_number = Column(String,unique=True)
    