import pytest
from app import app as flask_app

@pytest.fixture
def client(monkeypatch):
    """A test client for the app, with state reset for each test."""
    # Monkeypatch the global variables in the 'app' module to reset state
    monkeypatch.setattr('app.tasks', [
        {'id': 1, 'content': 'タスク管理ツールを作成する', 'done': False},
        {'id': 2, 'content': 'Flaskを勉強する', 'done': True}
    ])
    monkeypatch.setattr('app.next_id', 3)

    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_index_get(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    # Check for presence of key elements in Japanese (UTF-8 bytes)
    assert b'<h1>\xe3\x82\xbf\xe3\x82\xb9\xe3\x82\xaf\xe7\xae\xa1\xe7\x90\x86\xe3\x83\x84\xe3\x83\xbc\xe3\x83\xab</h1>' in response.data # <h1>タスク管理ツール</h1>
    assert b'Flask\xe3\x82\x92\xe5\x8b\x89\xe5\xbc\xb7\xe3\x81\x99\xe3\x82\x8b' in response.data # Flaskを勉強する

def test_add_task(client):
    """Test that a new task can be added."""
    response = client.post('/', data={'content': '新しいテストタスク'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'\xe6\x96\xb0\xe3\x81\x97\xe3\x81\x84\xe3\x83\x86\xe3\x82\xb9\xe3\x83\x88\xe3\x82\xbf\xe3\x82\xb9\xe3\x82\xaf' in response.data # 新しいテストタスク

def test_complete_task(client):
    """Test that a task can be marked as complete."""
    # Task 1 ('タスク管理ツールを作成する') is initially not done. Let's complete it.
    response = client.get('/complete/1', follow_redirects=True)
    assert response.status_code == 200
    # Check that the button now says '元に戻す' (Undo)
    assert b'\xe5\x85\x83\xe3\x81\xab\xe6\x88\xbb\xe3\x81\x99' in response.data # 元に戻す

def test_delete_task(client):
    """Test that a task can be deleted."""
    # Let's delete task 2 ('Flaskを勉強する')
    response = client.get('/delete/2', follow_redirects=True)
    assert response.status_code == 200
    # Check that the content of task 2 is no longer on the page
    assert b'Flask\xe3\x82\x92\xe5\x8b\x89\xe5\xbc\xb7\xe3\x81\x99\xe3\x82\x8b' not in response.data # Flaskを勉強する
