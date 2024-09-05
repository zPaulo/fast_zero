import pytest
from fastapi.testclient import TestClient  # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.models import Base
from fast_zero.database import get_session

@pytest.fixture
def client(session):
    def get_session_override():
        return session
    
    with TestClient(app) as client:  # Corrigido: 'client' com letra minúscula
        app.dependency_overrides[get_session] = get_session_override

        yield client  # Retorna a instância correta de 'client'
        
    app.dependency_overrides.clear()




@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
