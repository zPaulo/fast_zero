from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá mundoh'}


def test_create_user(client):
    response = client.post(  # UserSchema
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@email.com',
            'password': 'testsenha',
        },
    )

    # Voltou o status_code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar o UserPublic
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@email.com',
        'id': 1,
    }


def test_read_users(client):
    # Primeiro, cria um usuário
    client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@email.com',
            'password': 'testsenha',
        },
    )

    # Em seguida, faz uma solicitação para obter todos os usuários
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'testusername',
                'id': 1,
                'email': 'test@email.com',
            }
        ]
    }



def test_update_user(client):
    # Primeiro, cria um usuário
    create_response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@email.com',
            'password': 'testsenha',
        },
    )

    # Verifica se o usuário foi criado corretamente
    assert create_response.status_code == HTTPStatus.CREATED
    assert create_response.json() == {
        'username': 'testusername',
        'email': 'test@email.com',
        'id': 1,
    }

    # Agora, atualiza o usuário criado
    update_response = client.put(
        '/users/1',
        json={
            'username': 'testusername2',
            'email': 'aaaaaaaa@email.com',
            'password': '123',
        },
    )

    # Verifica se o usuário foi atualizado corretamente
    assert update_response.status_code == HTTPStatus.OK
    assert update_response.json() == {
        'username': 'testusername2',
        'email': 'aaaaaaaa@email.com',
        'id': 1,
    }


def test_delete_user(client):
    # Primeiro, cria um usuário
    client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@email.com',
            'password': 'testsenha',
        },
    )

    # Agora, deleta o usuário criado
    response = client.delete('/users/1')

    # Verifica se o usuário foi deletado corretamente
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}

