from chalice import Chalice
from src.auth import auth
from src.chats import chats
from src.messages import messages


"""
!!! IMPORTANT !!! 

nos services onde nao se passa email no verify_jwt_token 

ex: is_valid, message = verify_jwt_token(token)

se debe verificar manulmente se o usuário é dono do recurso

if chat["owner"] != get_email_from_token(token):
    return response("Unauthorized", {}, status_code=404)

!!! TODO 

- Melhorar a solucao de permissoes
- Subir arquivo pro bucket
- No service create-message integrar com open AI

"""

app = Chalice(app_name="auxiliAI")

app.register_blueprint(auth)
app.register_blueprint(chats)
app.register_blueprint(messages)
