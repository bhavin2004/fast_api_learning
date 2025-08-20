from fastapi import APIRouter,Depends,Path,HTTPException
from sqlalchemy.orm import Session
from ..models import Todo
from ..database import SessionLocal
from typing import Annotated
from starlette import status
from pydantic import BaseModel,Field
from .auth import get_current_user
 

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_config = Annotated[Session,Depends(connect_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get('/todos',status_code=status.HTTP_200_OK)
def get_all_todos(user:user_dependency,db:db_config):
    if not user or user['role'] != 'admin':
        raise HTTPException(401,"Authentocation Failed")
    
    res = db.query(Todo).all()
    if res:
        return res
    raise HTTPException(404,"NO RECORDS FOUND")

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user:user_dependency,
                db: db_config,todo_id : int = Path(gt=0)):
    if not user or user['role'] != 'admin':
        raise HTTPException(401,"Authentocation Failed")
 
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo_model:
        raise HTTPException(404,"Todo Not Found")
    print(db.query(Todo).filter(Todo.id == todo_id).delete())
    
    db.commit()