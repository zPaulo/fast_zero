from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Depends # type: ignore
from sqlalchemy import select

from fast_zero.models import User
from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema
from fast_zero.database import get_session

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundoh'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):

    db_user = session.scalar(
            select(User).where(
                (User.username == user.username) | (User.email == user.email))
        )
    
    if db_user:
            if db_user.username == user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Username already exist',
                )
            elif db_user.email == user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email already exist',
                )
        
        # Converte UserSchema para User, que é o objeto mapeado
    db_user = User(username=user.username, email=user.email, password=user.password)

    session.add(db_user)  # Adiciona o objeto User, não o UserSchema
    session.commit()
    session.refresh(db_user)

    return db_user
        

@app.get('/users/', response_model=UserList)
def read_users(session=Depends(get_session)):
    # Obter todos os usuários do banco de dados
    users = session.scalars(select(User)).all()
    return {'users': users}



@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    # Buscar o usuário no banco de dados
    db_user = session.get(User, user_id)
    
    # Verifica se o usuário existe
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    # Atualiza os campos do usuário
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    
    # Salva as mudanças no banco de dados
    session.commit()
    session.refresh(db_user)
    
    return db_user



@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session=Depends(get_session)):
    # Busca o usuário no banco de dados
    db_user = session.get(User, user_id)
    
    # Verifica se o usuário existe
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    # Deleta o usuário do banco de dados
    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
