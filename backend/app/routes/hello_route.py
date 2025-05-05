# Importações necessárias do Flask e Flask-Login
from flask_login import login_required
from flask import Blueprint, jsonify

# Importa serviços responsáveis pela lógica de Hello World
from ..services.hello_service import hello_world_service

# Cria um Blueprint chamado 'hello' para a rota de Hello World
hello_bp = Blueprint("hello", __name__)

# Rota de Hello World
@hello_bp.route("/hello_world", methods = ["GET"])
@login_required
def hello_world():
    result = hello_world_service()
    return jsonify(result), 200
