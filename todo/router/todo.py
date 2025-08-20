from fastapi import APIRouter,Depends,Path,HTTPException
from sqlalchemy.orm import Session
from ..models import Todo
from ..database import SessionLocal
from typing import Annotated
from starlette import status
from pydantic import BaseModel,Field
from .auth import get_current_user
 

router = APIRouter()


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_config = Annotated[Session,Depends(connect_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3,max_length=100)
    priority:int = Field(gt=0,lt=6)
    complete: bool = Field(default=False) 
   
@router.get("/",status_code=status.HTTP_200_OK)
def read_all(db: db_config,
             user:user_dependency):
    if not user:
        raise HTTPException(401,"Authentocation Failed")
      
    res = db.query(Todo).filter(Todo.owner_id == user['id']).all()
    if res:
        return res
    raise HTTPException(404,"NO RECORDS FOUND")

@router.get("/todo/{todo_id}")
def get_todo_by_id(user:user_dependency,db:db_config,todo_id:int = Path(gt=0)):
    if not user:
        raise HTTPException(401,"Authentocation Failed")
    
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user['id']).first()
    if todo_model: 
        return todo_model
    raise HTTPException(404,"Todo Not Found.")

@router.post('/todo', status_code=status.HTTP_201_CREATED)
def create_todo(user:user_dependency,db:db_config,todo_request: TodoRequest):

    if not user:
        raise HTTPException(401,"Authentocation Failed")

    todomodel =  Todo(**todo_request.model_dump(),owner_id = user['id'])
    
    db.add(todomodel)
    db.commit()
    
@router.put('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user:user_dependency,db:db_config, todo_req: TodoRequest, todo_id:int = Path(gt=0)):

    if not user:
        raise HTTPException(401,"Authentocation Failed")
 
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user['id']).first()
    if not todo_model:
        raise HTTPException(404,"Todo Not Found")
     
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.priority = todo_req.priority
    todo_model.complete = todo_req.complete
    
    db.add(todo_model)
    db.commit()
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user:user_dependency,
                db: db_config,todo_id : int = Path(gt=0)):
    if not user:
        raise HTTPException(401,"Authentocation Failed")
 
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user['id']).first()
    
    if not todo_model:
        raise HTTPException(404,"Todo Not Found")
    print(db.query(Todo).filter(Todo.id == todo_id).delete())
    
    db.commit()