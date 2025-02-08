from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criar aplicação Flask
app = Flask(__name__)

# Configuração da conexão com o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kiko:ff15dHpkRtuoNgeF8eWjpqymWLleEM00@dpg-ct76kgij1k6c73b3utk0-a.oregon-postgres.render.com/beachtennis"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criar instância do banco de dados
db = SQLAlchemy(app)

# Testar conexão
with app.app_context():
    try:
        db.engine.execute("SELECT nome_completo, data_nascimento, genero, telefone, email, endereco, data_cadastro FROM public.tb_clientes;")  # Executa um comando simples para testar
        print("✅ Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
