import bcrypt
from src.dao.user import get_user_password
import jwt
from datetime import datetime, timedelta
from src.utils.env import JWT_SECRET


def generate_hashed_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(email, password, hashed_password):
    # Aqui você faria a lógica para buscar o usuário com o email fornecido na tabela do DynamoDB
    # e obter a senha hashizada armazenada correspondente ao usuário
    # Vamos supor que você tenha uma função chamada 'get_user_password(email)' que retorna a senha hashizada armazenada
    stored_password = get_user_password(email)

    # Verifica se a senha fornecida corresponde à senha hashizada armazenada
    if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
        return True
    else:
        return False


# Função para gerar o token JWT
def generate_jwt_token(email):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Definir a expiração do token
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token.decode()


def verify_jwt_token(token, token_email=None):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email = payload.get("email")
        if not token_email:
            token_email = email
        if email != token_email:
            return False, "Unauthorized"
        if email:
            return True, email
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"

    return False, "Token verification failed"


def get_email_from_token(token):
    try:
        # Decodifica o token JWT e obtém as informações do payload
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

        # Obtém o email do usuário a partir do payload
        email = payload.get("email")
        return email

    except jwt.ExpiredSignatureError:
        # Lidar com o erro de token expirado, se necessário
        return None

    except jwt.InvalidTokenError:
        # Lidar com outros erros de token inválido, se necessário
        return None
