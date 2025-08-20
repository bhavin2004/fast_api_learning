from fastapi import APIRouter,Depends,HTTPException,Request
from pydantic import BaseModel,Field
from ..models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import timezone,datetime,timedelta
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'acaababb95bdcbf08fb1b608430c2fc3444a6b6b171b035e22845de0e142878b'
ALGO = 'HS256'

bcrypt_contest = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class UserRequest(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    password:str
    role:str
    phone_number:str = Field(min_length=10,max_length=10,default='1234567890')

def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_config = Annotated[Session,Depends(connect_db)]
templates = Jinja2Templates(directory="todo/templates")
def authenticate_user(username: str,pwd:str, db:db_config):
    user = db.query(Users).filter(Users.username == username).first()
    
    if not user:
        return False
    if not bcrypt_contest.verify(pwd, user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id: int , role:str,expire_delta: int):
    expire_delta:timedelta = timedelta(minutes=expire_delta)
    encode = {
         'sub': username,
         'id' : user_id,
         'role': role
    }
    
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,ALGO)

async def get_current_user(token: Annotated[str , Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGO)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')
        
        if username is None or user_id is None:
            raise HTTPException(401,"Could not validate user.")
        return {'username': username,'id':user_id,'role':role}
    except JWTError:
        raise HTTPException(401,"Could not validate user.")



@router.post('/',status_code=status.HTTP_201_CREATED)
def create_user(create_user_request: UserRequest,
                db: db_config):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
          first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_contest.hash(create_user_request   .password),
        is_active = True,
        role = create_user_request.role,
        phone_number = create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()
    
    # return create_user_model

@router.get('/login-page',status_code=200)
def get_login_page(request: Request):
    return (templates.TemplateResponse('login.html',{'request':request}))


@router.get('/register-page',status_code=200)
def render_register_page(request: Request):
    return templates.TemplateResponse('register.html',{'request':request})
@router.post("/token",status_code=status.HTTP_201_CREATED)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                           db:db_config):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(401,"Could not validate User.")
    token = create_access_token(user.username,user.id,user.role,20)
    return {"access_token": token, "token_type": "bearer"}

