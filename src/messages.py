from chalice import Blueprint
from src.utils.security import verify_jwt_token, get_email_from_token

from src.utils.api_utils import is_body_valid, response

from src.dao.message import insert_message, get_messages_by_chat
from src.dao.chat import update_chat_name, update_chat_file_text
from src.utils.bucket import send_file, generate_presigned_url
from src.auxiliai.openai_integration import (
    generate_response,
    format_to_openai_messages,
)
from src.utils.data_extractor import extract_text_from_base64_pdf

from src.dao.chat import get_chat
import uuid
import time
from datetime import datetime

messages = Blueprint(__name__)


@messages.route("/message", methods=["POST"], cors=True)
def create_message():
    start_time = time.time()
    token = messages.current_request.headers.get("Authorization", "")
    is_valid, message = verify_jwt_token(token)
    if not is_valid:
        return response(message, {}, status_code=401)

    required_fields = ["chat_id", "sender"]
    body = messages.current_request.json_body

    is_valid, message = is_body_valid(body, required_fields)

    if not is_valid:
        return response(message, {}, status_code=400)

    chat_id = body["chat_id"]
    chat = get_chat(chat_id)
    if not chat:
        return response("Chat not found", {}, status_code=404)

    if chat["owner"] != get_email_from_token(token):
        return response("Unauthorized", {}, status_code=404)

    message_id = str(uuid.uuid4())
    message_data = {
        "id": message_id,
        "chatId": chat_id,
        "owner": chat["owner"],
        "sender": body["sender"],
        "content": body["content"],  # mensagem ou nome do arquivo
        "file_url": body.get("file_url", ""),
        "is_file_message": False,
        "timestamp": datetime.now().isoformat(),
    }

    bot_message_data = {
        "id": str(uuid.uuid4()),
        "chatId": chat_id,
        "owner": "system",
        "sender": "system",
        "content": "",
        "file_url": "",
        "is_file_message": False,
        "timestamp": datetime.now().isoformat(),
    }

    if "file" in body:
        bucket_name = "files-auxiliai"
        file_format = "pdf"
        file_data = body["file"]
        file_path = f"message/{message_id}/doc.{file_format}"
        try:
            # ENVIA E EXTRAI TEXTO PDF
            send_file(file_format, file_data, file_path)

            file_url = generate_presigned_url(bucket_name, file_path)
            message_data["file_url"] = file_url
            message_data["file_text"] = extract_text_from_base64_pdf(file_data)

            promt_messages = [
                {
                    "role": "system",
                    "content": "Você é um assistente administrativo que analisa documentos",
                },
                {
                    "role": "system",
                    "content": message_data["file_text"],
                },
                {
                    "role": "system",
                    "content": "Responder com um resumo do conteúdo do PDF.",
                },
            ]

            # ATUALIZA INFORMACOES NO CHAT
            update_chat_name(chat_id, body["content"])
            update_chat_file_text(chat_id, message_data["file_text"])

            # GERA O RESUMO DO DOCUMENO
            bot_response, cost_message = generate_response(promt_messages)

            bot_message_data["content"] = bot_response
            bot_message_data["cost"] = cost_message

            message_data["summary_file"] = bot_response
            message_data["is_file_message"] = True

        except Exception as e:
            return response("Error uploading file", {}, status_code=500)
    else:
        question = body["content"]
        promt_messages = [
            {
                "role": "system",
                "content": "Você é um assistente administrativo que analisa documentos.",
            },
            {
                "role": "system",
                "content": chat["file_text"],
            },
            {
                "role": "user",
                "content": f"Responda a seguinte pergunta: {question}",
            },
        ]
        bot_response, cost_message = generate_response(promt_messages)
        bot_message_data["content"] = bot_response
        bot_message_data["cost"] = cost_message

    insert_message(message_data)
    insert_message(bot_message_data)

    messages_data = get_messages_by_chat(chat_id)
    filtered_messages_data = [
        {
            "file_url": message.get("file_url", ""),
            "content": message.get("content", ""),
            "timestamp": message.get("timestamp", ""),
            "sender": message.get("sender", ""),
            "id": message.get("id", ""),
        }
        for message in messages_data
    ]

    sorted_messages_data = sorted(filtered_messages_data, key=lambda x: x["timestamp"])
    return response("sucess", sorted_messages_data)


@messages.route("/messages/{email}/{chat_id}", cors=True)
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
    filtered_messages_data = [
        {
            "file_url": message.get("file_url", ""),
            "content": message.get("content", ""),
            "timestamp": message.get("timestamp", ""),
            "sender": message.get("sender", ""),
            "id": message.get("id", ""),
        }
        for message in messages_data
    ]

    sorted_messages_data = sorted(filtered_messages_data, key=lambda x: x["timestamp"])
    return response("sucess", sorted_messages_data)
