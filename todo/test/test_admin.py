from todo.main import app
from fastapi import status
from ..router.admin import get_current_user,connect_db
from .utils import overide_current_user,overide_get_db,client,test_data,TestingSessionLocal
from ..models import Todo

app.dependency_overrides[get_current_user] = overide_current_user
app.dependency_overrides[connect_db] = overide_get_db


def test_admin_read_all_todos(test_data):
    response = client.get("/admin/todos")
    assert response.status_code == 200
    
    db = TestingSessionLocal()
    
    assert response.json() == [{
           'complete': False,
           'description': 'Need to learn everyday!',
           'id': 1,
           'owner_id': 1,
           'priority': 5,
           'title': 'Learn to code!',
       }]
    

def test_admin_delete_todo(test_data):
    response = client.delete("/admin/todo/1")
    
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todo).filter_by(id=1).first()
    
    assert model is None
    
def test_admin_delete_todo_not_found(test_data):
    response = client.delete("/admin/todo/999")
    
    assert response.status_code == 404
    assert response.json() == {'detail':"Todo Not Found"}
    
