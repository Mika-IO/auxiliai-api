from chalice import Blueprint
from src.utils.security import verify_jwt_token, get_email_from_token

from src.utils.api_utils import is_body_valid, response

from src.dao.chat import insert_chat, delete_chat, get_chats_by_owner, get_chat
import uuid

from datetime import datetime

chats = Blueprint(__name__)


@chats.route("/chat", methods=["POST"], cors=True)
def create_chat():
    token = chats.current_request.headers.get("Authorization", "")
    is_valid, message = verify_jwt_token(token)
    if not is_valid:
        return response(message, {}, status_code=401)

    required_fields = ["owner", "name"]
    body = chats.current_request.json_body
    is_valid, message = is_body_valid(body, required_fields)

    if not is_valid:
        return response(message, {}, status_code=400)

    chat_data = {
        "id": str(uuid.uuid4()),
        "owner": body["owner"],
        "timestamp": datetime.now().isoformat(),
        "name": body["name"],
    }
    insert_chat(chat_data)
    return {"chat": chat_data}


@chats.route("/chats/{email}", cors=True)
def get_chats(email):
    token = chats.current_request.headers.get("Authorization", "")
    is_valid, message = verify_jwt_token(token, email)
    if not is_valid:
        return response(message, {}, status_code=401)

    chats_list = get_chats_by_owner(email)

    return response(
        "success",
        {
            "email": email,
            "chats": chats_list,
        },
        status_code=200,
    )


@chats.route("/chat/{chat_id}", methods=["DELETE"], cors=True)
def delete_chat_handler(chat_id):
    token = chats.current_request.headers.get("Authorization", "")
    is_valid, message = verify_jwt_token(token)
    if not is_valid:
        return response(message, {}, status_code=401)

    # Obter o chat pelo ID
    chat = get_chat(chat_id)

    if chat is None:
        return response("Chat not found", {}, status_code=404)

    delete_chat(chat_id)
    return response("Chat deleted successfully")
