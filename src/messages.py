from chalice import Blueprint
from src.utils.security import verify_jwt_token, get_email_from_token

from src.utils.api_utils import is_body_valid, response

from src.dao.message import insert_message, get_messages_by_chat

from src.dao.chat import get_chat
import uuid

from datetime import datetime

messages = Blueprint(__name__)


@messages.route("/message", methods=["POST"])
def create_message():
    token = messages.current_request.headers.get("Authorization", "")
    is_valid, message = verify_jwt_token(token)
    if not is_valid:
        return response(message, {}, status_code=401)

    required_fields = ["chat_id", "sender", "content"]
    body = messages.current_request.json_body
    is_valid, message = is_body_valid(body, required_fields)

    if not is_valid:
        return response(message, {}, status_code=400)

    # Verifique se o chat existe e pertence ao usuário autenticado
    chat_id = body["chat_id"]
    chat = get_chat(chat_id)
    if not chat:
        return response("Chat not found", {}, status_code=404)

    if chat["owner"] != get_email_from_token(token):
        return response("Unauthorized", {}, status_code=404)

    # Crie a mensagem com os dados fornecidos
    message_data = {
        "id": str(uuid.uuid4()),
        "chatId": chat_id,
        "owner": chat["owner"],
        "sender": body["sender"],
        "content": body["content"],
        "file_url": body.get("file_url", ""),
        "timestamp": datetime.now().isoformat(),
    }
    insert_message(message_data)

    return {"message": message_data}


@messages.route("/messages/{email}/{chat_id}")
def get_messages(email, chat_id):
    token = messages.current_request.headers.get("Authorization", "")
    is_valid, message = verify_jwt_token(token, token_email=email)
    if not is_valid:
        return response(message, {}, status_code=401)

    # Verifique se o chat existe e pertence ao usuário autenticado
    chat = get_chat(chat_id)
    if not chat:
        return response("Chat not found", {}, status_code=404)

    # Obtenha as mensagens associadas ao chat
    messages_data = get_messages_by_chat(chat_id)
    return response("sucess", messages_data)
