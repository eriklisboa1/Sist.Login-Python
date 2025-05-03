from flask import Blueprint, request, jsonify
from email_validator import validate_email, EmailNotValidError
from models import db, User, bcrypt

routes = Blueprint('routes', __name__)

def senha_forte(senha):
    import re
    return (len(senha) >= 8 and
            re.search(r"[A-Z]", senha) and
            re.search(r"[a-z]", senha) and
            re.search(r"[0-9]", senha) and
            re.search(r"[!@#$%^&*]", senha))

@routes.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        return jsonify({'erro': 'Email inválido'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'erro': 'Email já cadastrado'}), 409

    if not senha_forte(data['senha']):
        return jsonify({'erro': 'Senha fraca. Use letras maiúsculas, minúsculas, números e símbolos.'}), 400

    hashed_password = bcrypt.generate_password_hash(data['senha']).decode('utf-8')

    novo_usuario = User(
        nome=data['nome'],
        cpf=data['cpf'],
        endereco=data['endereco'],
        email=data['email'],
        senha=hashed_password
    )

    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário registrado com sucesso'}), 201

@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = User.query.filter_by(email=data['email']).first()
    if usuario and usuario.verificar_senha(data['senha']):
        return jsonify({'mensagem': 'Login bem-sucedido'}), 200
    return jsonify({'erro': 'Credenciais inválidas'}), 401
