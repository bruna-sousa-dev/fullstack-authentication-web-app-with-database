# Importações necessárias do Flask e Flask-Login
from flask import Blueprint, request, jsonify, session, render_template_string
from flask_login import login_required, current_user

# Importa serviços responsáveis pela lógica de autenticação
from app.services.auth_service import (
    login_user_service,
    logout_user_service,
    check_session_service,
    register_user_service,
    list_users_service,
    edit_user_service,
    get_test_user_service,
    del_user_service
)

# Cria um Blueprint chamado 'auth' para agrupar as rotas de autenticação
auth_bp = Blueprint("auth", __name__)

# Rota de login: espera username e password, utiliza o serviço para autenticar
@auth_bp.route("/login", methods = ["POST"])
def login():
    from ..models.db_user_model import User  # Importação local para evitar importações circulares
    from app import db
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    result = login_user_service(User, username, password, db)
    if result.get("success"):
        return jsonify(result), 200  # Sucesso: usuário autenticado
    return jsonify(result), 401     # Falha na autenticação

# Rota de logout: exige login prévio, finaliza a sessão do usuário
@auth_bp.route("/logout", methods = ["GET"])
@login_required
def logout():
    result = logout_user_service()
    return jsonify(result), 200

# Rota para verificar se a sessão do usuário ainda está válida
@auth_bp.route("/check_session", methods = ["GET"])
def check_session():
    result = check_session_service()
    status_code = 200 if result["logged_in"] else 401  # Retorna 401 se não estiver logado
    return jsonify(result), status_code

# Rota para depuração: exibe o conteúdo atual da sessão (útil em desenvolvimento)
@auth_bp.route("/debug_session", methods = ["GET"])
def debug_session():
    return jsonify({"session": dict(session)})

# Rota de registro de novo usuário: apenas usuários logados e autorizados podem registrar outros
@auth_bp.route("/register", methods = ["POST"])
@login_required
def register():
    from ..models.db_user_model import User
    from app import db  # Importações locais para evitar ciclos
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    result = register_user_service(User, db, current_user, username, password)

    # Caso ocorra erro na tentativa de registrar
    if result.get("error"):
        return jsonify(result), 400
    
    # Caso não seja autorizado
    elif result.get("unauthorized"):
        return jsonify(result), 401

    # Registro realizado com sucesso
    return jsonify(result), 201

# Rota para listar todos os usuários do sistema (somente para usuários logados)
@auth_bp.route("/users", methods = ["GET"])
@login_required
def list_users():
    from ..models.db_user_model import User
    users_list = list_users_service(User)
    return jsonify({"users": users_list}), 200

# Rota para edição de um usuário específico (identificado por username atual)
@auth_bp.route("/edit_user/<string:current_username>", methods = ["PUT"])
@login_required
def edit_user(current_username):
    from ..models.db_user_model import User
    from app import db
    data = request.get_json()
    new_username = data.get("username")
    new_password = data.get("password")

    # Executa serviço de edição e trata retorno
    result = edit_user_service(User, db, current_user, current_username, new_username, new_password)
    
    if result.get("error"):
        return jsonify(result), 404  # Usuário não encontrado

    # Caso não seja autorizado
    elif result.get("unauthorized"):
        return jsonify(result), 401

    return jsonify(result), 200  # Edição bem-sucedida

# Rota para obter o usuario de teste presente no db
@auth_bp.route("/get_test_user", methods = ["GET"])
def get_user_test():
    from ..models.db_user_model import User
    result = get_test_user_service(User)
    return jsonify(result), 200 

# Rota para exclusão de usuário
@auth_bp.route("/del_user", methods = ["POST"])
def del_user():
    from ..models.db_user_model import User
    from app import db
    data = request.get_json()
    del_user = data.get("username")

    result = del_user_service(User, db, current_user, del_user)

    if result.get("error"):
        return jsonify(result), 404  # Usuário não encontrado

    # Caso não seja autorizado
    elif result.get("unauthorized"):
        return jsonify(result), 401

    return jsonify(result), 200  # Exclusão bem-sucedida
