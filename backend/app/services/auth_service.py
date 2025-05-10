# Importações do Flask-Login para gerenciar sessões de usuário
from flask_login import login_user, logout_user, current_user
# Importações para criação do usuário de administrador
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash

# Serviço para realizar login de um usuário
def login_user_service(User, username, password, db):
    # Busca o usuário no banco de dados pelo nome de usuário
    user = User.query.filter_by(username = username).first()
    
    # Se o usuário existe e a senha está correta, realiza login
    if user and user.check_password(password):
        login_user(user)  # Função do Flask-Login que registra o login do usuário
        # Atualiza contadores e persiste no banco
        current_user.login_count += 1
        db.session.commit()
        return {"success": True, "message": "Login realizado com sucesso!", "username": username}
    
    # Se usuário não existe ou senha incorreta
    return {"success": False, "error": "Usuário ou senha incorretos"}

# Serviço para realizar logout do usuário atual
def logout_user_service():
    logout_user()  # Função do Flask-Login que finaliza a sessão
    return {"message": "Logout realizado!"}

# Serviço para verificar se há um usuário autenticado na sessão atual
def check_session_service():
    if current_user.is_authenticated:
        # Se o usuário está logado, retorna o nome de usuário
        return {"logged_in": True, "username": current_user.username}
    # Caso contrário, retorna que não há usuário logado
    return {"logged_in": False}

# Serviço para registrar um novo usuário no sistema (restrito a usuários autorizados)
def register_user_service(User, db, current_user, username, password):
    # Verifica se o usuário atual tem permissão para registrar outros (admin hardcoded)
    if current_user.username not in ["admin@mail.com"]:
        return {"unauthorized": "Somente o administrador pode realizar o cadastro de novos usuários!"}

    # Verifica se os campos obrigatórios foram preenchidos
    if not username or not password:
        return {"error": "usuário e senha são obrigatórios!"}
    
    # Verifica se o nome de usuário já está cadastrado
    if User.query.filter_by(username=username).first():
        return {"error": "Usuário já existe!"}
    
    # Cria novo usuário, define a senha e salva no banco de dados
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "Usuário registrado com sucesso!"}

# Serviço para listar todos os usuários cadastrados
def list_users_service(User):
    users = User.query.all()
    # Retorna uma lista com dados públicos de cada usuário
    return [{"id": user.id, "username": user.username, "login_count": user.login_count} for user in users]

# Serviço para editar os dados de um usuário existente
def edit_user_service(User, db, current_user, current_username, new_username=None, new_password=None):
    
    # Busca o usuário pelo nome atual
    user = User.query.filter_by(username=current_username).first()

    if current_user.username not in ["admin@mail.com"]:
        return {"unauthorized": "Somente o administrador pode editar o usuário do administrador!"}

    # Se o usuário não foi encontrado, retorna erro
    if not user:
        return {"error": "Usuário não encontrado!"}

    # Atualiza o nome de usuário, se informado
    if new_username:
        user.username = new_username
    # Atualiza a senha, se informada
    if new_password:
        user.set_password(new_password)
    
    # Salva alterações no banco de dados
    db.session.commit()

    return {"message": "Usuário atualizado com sucesso!"}

def get_test_user_service(User):
    # Busca o usuário pelo id de teste
    test_user = User.query.filter_by(id = 2).first()
    return {"username": test_user.username}

def del_user_service(User, db, current_user, del_user):
    # Busca o usuário no banco de dados
    user = User.query.filter_by(username = del_user).first()

    if current_user.username not in ["admin@mail.com"]:
        return {"unauthorized": "Somente o administrador pode excluir usuários! ;)"}
    
    # Se o usuário não foi encontrado, retorna erro
    if not user:
        return {"error": "Usuário não encontrado!"}
    
    db.session.delete(user)
    db.session.commit()

    return {"message": "Usuário excluído com sucesso!"}

def create_default_user_service(User, db):
    load_dotenv()
    default_email = "admin@mail.com"
    default_password = os.getenv("DEFAULT_PASSWORD")
    default_password_hash = generate_password_hash(default_password)

    user = User.query.filter_by(username = default_email).first()
    if not user:
        new_user = User(username = default_email, password_hash = default_password_hash)
        db.session.add(new_user)
        db.session.commit()