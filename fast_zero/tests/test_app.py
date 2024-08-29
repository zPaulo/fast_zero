from fastapi.testclient import TestClient
from http import HTTPStatus
from fast_zero.app import app

client = TestClient(app)


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app) # Arrange (organização)

    response = client.get ('/') # Act (Ação)

    assert response.status_code == HTTPStatus.OK # Assert 
    assert response.json() == {'message': 'Olá mundoh'}