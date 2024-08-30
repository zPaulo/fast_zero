from fastapi import FastAPI
from fast_zero.schemas import Message, UserSchema, UserPublic
from http import HTTPStatus

app = FastAPI()

database = []

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundoh'}

@app.post('/users/',status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    return user
