from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

""" 
    Define o modelo de usuário para o banco de dados, herdando de UserMixin (para integração com Flask-Login)
    e db.Model (para integração com SQLAlchemy)
"""
class User(UserMixin, db.Model):

    # Coluna 'id' será a chave primária (identificador único do usuário)
    id = db.Column(db.Integer, primary_key=True)

    # Nome de usuário único e obrigatório (não pode ser nulo)
    username = db.Column(db.String(100), unique=True, nullable=False)

    # Hash da senha do usuário (não armazena a senha em texto claro)
    password_hash = db.Column(db.String(255), nullable=False)

    # Contador de logins do usuário, começa em 0 e não pode ser nulo
    login_count = db.Column(db.Integer, default=0, nullable=False)

    # Método para definir a senha do usuário convertendo-a em hash seguro
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Método para verificar se a senha fornecida corresponde ao hash armazenado
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
