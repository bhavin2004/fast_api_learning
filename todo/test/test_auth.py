from todo.main import app
from fastapi import status
from ..router.auth import get_current_user,connect_db,bcrypt_contest,authenticate_user,create_access_token,SECRET_KEY,ALGO
from .utils import overide_current_user,overide_get_db,client,test_data,test_user,TestingSessionLocal
from ..models import Users
from jose import jwt
import pytest
from fastapi import HTTPException
app.dependency_overrides[get_current_user] = overide_current_user
app.dependency_overrides[connect_db] = overide_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    
    authenticated_user = authenticate_user(test_user.username,'testpassword',db)
    assert authenticated_user is not None
    
    non_existed_user = authenticate_user("WrongUser",'testpassword',db)
    assert non_existed_user is False
    
    
    wrong_password_user = authenticate_user(test_user.username,'wrongpassword',db)
    assert wrong_password_user is False
    
def test_create_access_token(test_user):
    username = 'testuser'
    user_id = 1
    role = 'user'
    expire_delta = 20
    
    token = create_access_token(username,user_id,role,expire_delta)
    
    decode_token = jwt.decode(token,SECRET_KEY,algorithms=[ALGO])
    
    assert decode_token['sub'] == username  
    assert decode_token['id'] == user_id  
    assert decode_token['role'] == role  
    
@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGO)
    
    user = await get_current_user(token=token)
    
    assert user == {'username': 'testuser', 'id': 1, 'role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGO)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user.'
    
def test_create_user(test_user):
    request_data = {
                    "email": "test@example.com",
                    "username": "test",
                    "first_name": "test",
                    "last_name": "test",
                    "password": "12345678",
                    "role": "user",
                    "phone_number": "1234567890"
                    }
    response = client.post('/auth',json=request_data)
    
    assert response.status_code == 201
    db = TestingSessionLocal()
    
    model = db.query(Users).filter_by(id=2).first()
    
    assert model is not None