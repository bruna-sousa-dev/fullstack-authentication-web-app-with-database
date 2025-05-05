from dotenv import load_dotenv
import os

load_dotenv() # Lê as variáveis de embiente presentes no arquivo .env

# Parâmetros de configuração do app Flask
class ConfigAppFlask:
    
    # Chave secreta usada para proteger sessões e cookies; usa variável de ambiente ou uma chave padrão
    SECRET_KEY = os.getenv("SECRET_KEY", "MPzkAeG7zChV2Jo3y6OvlUyzBCh54q745eUX15IcZhr")

    # Configurações de sessão do Flask
    SESSION_TYPE = 'filesystem'  # Armazena sessões no sistema de arquivos
    SESSION_FILE_DIR = os.path.join(os.getcwd(), "backend/sessions")  # Caminho onde os arquivos de sessão serão salvos
    SESSION_PERMANENT = False  # Sessão expira ao fechar o navegador
    SESSION_USE_SIGNER = True  # Protege os dados da sessão com assinatura criptográfica
    SESSION_COOKIE_NAME = 'example_session'  # Nome do cookie da sessão
    SESSION_COOKIE_HTTPONLY = True  # Impede acesso ao cookie via JavaScript (proteção contra XSS)
    SESSION_COOKIE_SECURE = True  # Cookie só é transmitido via HTTPS (proteção contra sniffing)
    SESSION_COOKIE_SAMESITE = "None"  # Permite o envio do cookie entre sites (necessário para apps em domínios diferentes)
    SESSION_COOKIE_PATH = "/"  # Torna o cookie acessível para toda a aplicação

    # Configuração do banco de dados SQLite via SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///users.db')  # Usa variável de ambiente ou banco local
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa rastreamento de modificações para melhorar desempenho e evitar alertas

# Aplica CORS (Cross-Origin Resource Sharing) à aplicação Flask
def apply_cors(app):
    # Define um manipulador que será executado após cada resposta da aplicação
    @app.after_request
    def add_cors_headers(response):
        
        # Adiciona o cabeçalho 'Access-Control-Allow-Origin' apenas se ainda não estiver presente
        if "Access-Control-Allow-Origin" not in response.headers:
            response.headers["Access-Control-Allow-Origin"] = "https://meu-dominio.com"  # Permite requisições apenas desse domínio

        # Permite o envio de cookies e autenticação entre domínios
        response.headers["Access-Control-Allow-Credentials"] = "true"

        # Especifica os métodos HTTP permitidos nas requisições CORS
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"

        # Define os cabeçalhos permitidos nas requisições CORS
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        # Retorna a resposta modificada com os cabeçalhos CORS
        return response

# Função para configurar o login manager do Flask-Login
def configure_login_manager(login_manager, User):
    
    # Define a função responsável por carregar um usuário a partir do ID armazenado na sessão
    @login_manager.user_loader
    def load_user(user_id):
        # Consulta o banco de dados e retorna o usuário com o ID fornecido
        return User.query.get(int(user_id))
