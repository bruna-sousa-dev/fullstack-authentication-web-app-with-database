# Importações dos principais módulos do Flask e extensões utilizadas
from flask import Flask
from flask_cors import CORS  # Permite requisições entre diferentes domínios (Cross-Origin Resource Sharing)
from flask_login import LoginManager  # Gerencia autenticação de usuários
from flask_sqlalchemy import SQLAlchemy  # ORM para interagir com bancos de dados relacionais

# Importa configurações e funções auxiliares
from .services.config_flask_service import ConfigAppFlask, apply_cors, configure_login_manager

# Instancia objetos globais das extensões, mas sem associá-los ainda ao app
db = SQLAlchemy()
login_manager = LoginManager()

# Função que cria e configura a aplicação Flask
def create_app():

    app = Flask(__name__)  # Cria a instância do app Flask

    # Carrega as configurações da classe ConfigAppFlask
    app.config.from_object(ConfigAppFlask)

    # Inicializa as extensões com o app já criado
    db.init_app(app)
    login_manager.init_app(app)

    # Configura o CORS para permitir requisições de outros domínios, incluindo envio de cookies
    CORS(app, supports_credentials = True, methods = ["GET", "POST", "PUT", "OPTIONS"])
    
    # Aplica cabeçalhos de CORS personalizados após cada resposta
    apply_cors(app)

    # Importa o modelo User e configura a função que carrega usuários para sessões do Flask-Login
    from .models.db_user_model import User
    configure_login_manager(login_manager, User)

    # Cria as tabelas no banco de dados dentro do contexto da aplicação
    with app.app_context():
        db.create_all()

    # Importa as rotas da aplicação
    # from app.routes import routes_auth, route_hello_world
    from .routes.auth_route import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.hello_route import hello_bp
    app.register_blueprint(hello_bp)

    return app  # Retorna a aplicação Flask configurada
