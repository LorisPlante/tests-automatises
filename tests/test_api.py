import pytest
from app import create_app

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    app = create_app({
        'TESTING': True,
        'DATABASE': str(db_path)
    })
    with app.test_client() as client:
        yield client

def test_create_app_default_config():
    app = create_app()
    assert app is not None

def test_api_test_endpoint(client):
    response = client.get('/api/test')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'API fonctionne correctement'

def test_before_and_teardown(client):
    response = client.get('/api/test')
    assert response.status_code == 200

# ----------- CALCULATRICE -----------

def test_add(client):
    response = client.get('/api/add/2/3')
    assert response.status_code == 200
    assert response.get_json()['result'] == 5

def test_subtract_invalid_input(client):
    response = client.get('/api/subtract/x/y')
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_subtract_invalid_input_force(client):
    response = client.get('/api/subtract/a/b')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Les paramètres doivent être des nombres'

def test_multiply_invalid_input(client):
    response = client.get('/api/multiply/hello/world')
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_multiply_invalid_input_force(client):
    response = client.get('/api/multiply/a/b')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Les paramètres doivent être des nombres'

def test_divide_invalid_input(client):
    response = client.get('/api/divide/foo/bar')
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_divide_invalid_input_force(client):
    response = client.get('/api/divide/a/1')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Les paramètres doivent être des nombres'

def test_divide_by_zero(client):
    response = client.get('/api/divide/10/0')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Division par zéro impossible'

# ----------- UTILISATEURS -----------

def test_user_creation(client):
    response = client.post('/api/user', json={
        'username': 'john',
        'email': 'john@example.com'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Utilisateur ajouté avec succès'

def test_user_creation_duplicate(client):
    client.post('/api/user', json={'username': 'jane', 'email': 'jane@example.com'})
    response = client.post('/api/user', json={'username': 'jane', 'email': 'jane@example.com'})
    assert response.status_code == 409
    assert 'error' in response.get_json()

def test_add_user_missing_fields(client):
    response = client.post('/api/user', json={'username': 'incomplete'})
    assert response.status_code == 400

def test_user_fetch_success(client):
    client.post('/api/user', json={'username': 'mark', 'email': 'mark@example.com'})
    response = client.get('/api/user/mark')
    assert response.status_code == 200
    assert response.get_json()['email'] == 'mark@example.com'

def test_user_fetch_not_found(client):
    response = client.get('/api/user/ghost')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Utilisateur non trouvé'

def test_user_get_not_found_explicit(client):
    response = client.get('/api/user/someone-who-doesnt-exist')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Utilisateur non trouvé'

def test_user_deletion_success(client):
    client.post('/api/user', json={'username': 'lucas', 'email': 'lucas@example.com'})
    response = client.delete('/api/user/lucas')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Utilisateur supprimé avec succès'

def test_user_deletion_not_found(client):
    response = client.delete('/api/user/invisible')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Utilisateur non trouvé'

def test_subtract_value_error(client):
    response = client.get('/api/subtract/foo/5')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Les paramètres doivent être des nombres'

def test_multiply_value_error(client):
    response = client.get('/api/multiply/bar/2')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Les paramètres doivent être des nombres'

def test_divide_value_error(client):
    response = client.get('/api/divide/baz/2')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Les paramètres doivent être des nombres'

def test_user_not_found_json(client):
    response = client.get('/api/user/inexistant')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Utilisateur non trouvé'


# ----------- MOCKS -----------

def test_add_user_mocked(mocker, client):
    mocker.patch('app.api.db', autospec=True)
    mocker.patch('app.api.db.add_user', return_value=True)

    response = client.post('/api/user', json={
        'username': 'mocky',
        'email': 'mocky@example.com'
    })

    assert response.status_code == 201
    assert response.get_json()['message'] == 'Utilisateur ajouté avec succès'

def test_add_user_mocked_fail(mocker, client):
    mocker.patch('app.api.db', autospec=True)
    mocker.patch('app.api.db.add_user', return_value=False)

    response = client.post('/api/user', json={
        'username': 'failuser',
        'email': 'fail@example.com'
    })

    assert response.status_code == 409
    assert 'error' in response.get_json()
