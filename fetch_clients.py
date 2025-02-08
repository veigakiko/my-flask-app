from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criar aplicação Flask
app = Flask(__name__)

# Configuração da conexão com o PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kiko:ff15dHpkRtuoNgeF8eWjpqymWLleEM00@dpg-ct76kgij1k6c73b3utk0-a.oregon-postgres.render.com/beachtennis"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criar instância do banco de dados
db = SQLAlchemy(app)

# Função para buscar clientes
def fetch_clients():
    query = """
    SELECT nome_completo, data_nascimento, genero, telefone, email, endereco, data_cadastro
    FROM public.tb_clientes;
    """
    
    with app.app_context():
        try:
            results = db.engine.execute(query)
            clientes = results.fetchall()  # Pega todos os registros

            print("✅ Dados dos clientes encontrados:")
            for cliente in clientes:
                print(cliente)

        except Exception as e:
            print(f"❌ Erro ao buscar clientes: {e}")

# Chamar a função
if __name__ == "__main__":
    fetch_clients()
