from fastapi import APIRouter,Depends,Path,HTTPException,Request
from sqlalchemy.orm import Session
from ..models import Todo
from ..database import SessionLocal
from typing import Annotated
from starlette import status
from pydantic import BaseModel,Field
from .auth import get_current_user
from starlette.responses import  RedirectResponse
from fastapi.templating import  Jinja2Templates
 

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_config = Annotated[Session,Depends(connect_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
templates = Jinja2Templates(directory="todo/templates")
class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3,max_length=100)
    priority:int = Field(gt=0,lt=6)
    complete: bool = Field(default=False)


def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page',status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response


##Pages
@router.get("/todo-page",status_code=200)
async def render_todo_page(request: Request,db: db_config):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()

        todos = db.query(Todo).filter(Todo.owner_id == user.get('id')).all()

        return templates.TemplateResponse('todo.html',{'request':request,'todos':todos,'user':user})
    except:
        return redirect_to_login()


@router.get('/add-todo-page',status_code=200)
async def add_todo_page(request: Request,db: db_config):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse('add-todo.html',{'request':request,'user':user})
    except:
        return redirect_to_login()

@router.get('/edit-todo-page/{todo_id}',status_code=200)
async def edit_todo_page(request: Request,db: db_config, todo_id: int):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        return templates.TemplateResponse('edit-todo.html',{'request':request,'user':user,'todo':todo})
    except:
        return redirect_to_login()



## API ENDPOINTS
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