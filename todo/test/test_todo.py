
from todo.main import app
from fastapi import status
from ..router.todo import get_current_user,connect_db
from .utils import overide_current_user,overide_get_db,client,test_data,TestingSessionLocal
from ..models import Todo

app.dependency_overrides[get_current_user] = overide_current_user
app.dependency_overrides[connect_db] = overide_get_db



def test_read_all_authenticated(test_data):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ==[{'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday!', 'id': 1,
                                'priority': 5, 'owner_id': 1}]
    
def test_read_one_authenticated(test_data):
    response = client.get('/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() =={'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday!', 'id': 1,
                                'priority': 5, 'owner_id': 1}
    

def test_read_one_authenticated_not_found(test_data):
    response = client.get('/todo/99')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Todo Not Found.'}
    
    
def test_create_todo(test_data):
    request_data={
        'title': 'New Todo!',
        'description':'New todo description',
        'priority': 5,
        'complete': False,
    }
    response = client.post("/todo",json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 2).first()
    
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.priority == request_data['priority']
    assert model.complete == request_data['complete']
    
    return

def test_update_todo(test_data):    
    request_data={
        'title': 'New Todo!',
        'description':'New todo description',
        'priority': 5,
        'complete': False,
    }
    response = client.put("/todo/1",json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.priority == request_data['priority']
    assert model.complete == request_data['complete']
    
    return

def test_update_todo_not_found(test_data):    
    request_data={
        'title': 'New Todo!',
        'description':'New todo description',
        'priority': 5,
        'complete': False,
    }
    response = client.put("/todo/999",json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':"Todo Not Found"}
    return

def test_delete_todo(test_data):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    
    assert model is None
    
def test_delete_todo_not_found(test_data):
    response = client.delete("/todo/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':"Todo Not Found"}
    

