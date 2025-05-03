from flask import Blueprint, request, jsonify
from email_validator import validate_email, EmailNotValidError
from models import db, User, bcrypt
import jwt
import datetime
import os
from utils import enviar_email_confirmacao

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

    token = jwt.encode({
        'user_id': novo_usuario.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, os.getenv("SECRET_KEY"), algorithm='HS256')

    enviado = enviar_email_confirmacao(novo_usuario.email, token)

    if not enviado:
        return jsonify({'erro': 'Erro ao enviar email de confirmação'}), 500

    return jsonify({'mensagem': 'Usuário registrado. Verifique seu email para confirmar.'}), 201

@routes.route('/confirmar_email/<token>', methods=['GET'])
def confirmar_email(token):
    try:
        dados = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
        usuario = User.query.get(dados['user_id'])

        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        if usuario.confirmado:
            return jsonify({'mensagem': 'Email já confirmado'}), 200

        usuario.confirmado = True
        db.session.commit()

        return "<h3>Email confirmado com sucesso! Agora você pode fazer login.</h3>", 200

    except jwt.ExpiredSignatureError:
        return "<h3>Token expirado. Solicite um novo registro.</h3>", 400
    except jwt.InvalidTokenError:
        return "<h3>Token inválido.</h3>", 400

@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = User.query.filter_by(email=data['email']).first()

    if not usuario:
        return jsonify({'erro': 'Credenciais inválidas'}), 401

    if not usuario.confirmado:
        return jsonify({'erro': 'Email não confirmado. Verifique sua caixa de entrada.'}), 403

    if usuario.verificar_senha(data['senha']):
        return jsonify({'mensagem': 'Login bem-sucedido'}), 200

    return jsonify({'erro': 'Credenciais inválidas'}), 401
