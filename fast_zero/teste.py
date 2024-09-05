from sqlalchemy import create_engine

# String de conexão do banco de dados
engine = create_engine('sqlite:///database.db')

# Criar conexão para verificar se o arquivo é criado
with engine.connect() as connection:
    result = connection.execute("SELECT 1")
    print(result.fetchone())
