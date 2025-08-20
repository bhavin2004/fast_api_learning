from todo.main import app
from fastapi import status
from ..router.user import get_current_user,connect_db,bcrypt_contest
from .utils import overide_current_user,overide_get_db,client,test_data,TestingSessionLocal
from ..models import Users

app.dependency_overrides[get_current_user] = overide_current_user
app.dependency_overrides[connect_db] = overide_get_db

def test_get_user_details(test_data):
    response = client.get("/user")
    
    assert response.status_code == 200
    assert response.json()['username'] == 'codingwithrobytest'
    assert response.json()['email'] == 'codingwithrobytest@email.com'
    assert response.json()['first_name'] == 'Eric'
    assert response.json()['last_name'] == 'Roby'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-1111'
    
    return

def test_user_change_password(test_data):
    request_data = {"current_pwd":"testpassword",
                    "new_pwd":"12345678"}
    
    response = client.put("/user/change_password",json=request_data)

    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Users).first()
    assert bcrypt_contest.verify(request_data['new_pwd'], model.hashed_password) is True

def test_user_change_password_invalid_current_password(test_data):
    request_data = {"current_pwd":"wrongpassword",
                    "new_pwd":"12345678"}
    
    response = client.put("/user/change_password",json=request_data)

    assert response.status_code == 401
    assert response.json() == {'detail':"Wrong Current Password"}
      


def test_user_change_phone_number(test_data):
    
    response = client.put("/user/change_phone_number/1234567890")

    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Users).first()
    assert model.phone_number=="1234567890"

