from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader


from models import TokenRequest, Chat
from utils import response
import uuid

from fake_db import chats, messages

app = FastAPI()
api_key_header = APIKeyHeader(name="Authorization")


API_KEY = "TOKEN"

# TOKEN


@app.post("/token")
def create_token(request: TokenRequest):
    email = request.email
    password = request.password

    # Aqui você pode realizar a verificação do email e senha
    # e gerar um token de autenticação válido

    # Exemplo simplificado: Verificar se o email é "admin@example.com" e a senha é "password"
    if email == "mikaiodev@gmail.com" and password == "ytbr5678":
        API_KEY = "TOKEN"
        return {"token": API_KEY}

    # Caso as credenciais não sejam válidas, retornar um erro
    return response("invalid credentials", {}, status_code=401)


# CHATS


@app.get("/chats")
def get_chats(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return response("success", chats)


@app.get("/chat/{id}")
def get_chat_by_id(id: str, api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    for chat in chats:
        if chat["id"] == id:
            return response("success", chat)
    return response("chat not found", {}, status_code=404)


@app.post("/chat")
def create_chat(chat: Chat, api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    new_chat = {
        "id": str(uuid.uuid4()),
        "name": chat.name,
        "owner_id": chat.owner_id,
    }
    chats.append(new_chat)
    return response("success", new_chat, status_code=201)


# MESSAGES


@app.get("/messages")
def get_messages(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return response("success", messages)


@app.get("/message/{id}")
def get_message_by_id(id: str, api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    for message in messages:
        if message["id"] == id:
            return response("success", message)
    return response("message not found", {}, status_code=404)
