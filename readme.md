# Auxiliai

A GPT tool to analize PDF documents

#### Getting Started

```shell
  # Set up a virtual environment:

  python3 -m venv virtualenv

  # Activate the environment:

  source virtualenv/bin/activate

  # Install the dependencies:

  pip install -r requirements.txt

  # Run the API with Uvicorn:

  uvicorn src.main:app --reload
```

#### Endpoits

- POST -> Token
- POST -> PDF file
- POST -> Chat
- POST -> Message
- GET -> Chats
- GET -> Messages
- DELETE -> Chats

#### Models

ACCOUNT USERS

```json
{
  "id": "1235678910-2bfc-4fc7-bf12-49f07c877b997",
  "email": "mikaiodev@gmail.com",
  "username": "Mikaio",
  "role": "admin",
  "administrator_id": "1235678910-2bfc-4fc7-bf12-49f07c877b997",
  "hashed_password": "hashed_password"
}
```

CHAT

```json
{
  "id": "76d2e3293c-2bfc-4fc7-bf12-49f07c877b997",
  "owner_id": "1235678910-2bfc-4fc7-bf12-49f07c877b997",
  "timestamp": "2023-07-05T10:30:00Z",
  "name": "Chat de Exemplo"
}
```

PDF FILES

```json
{
  "id": "d2e3293c-2bfc-4fc7-bf12-49f07c877b22",
  "chatId": "76d2e3293c-2bfc-4fc7-bf12-49f07c877b997",
  "timestamp": "2023-07-05T10:30:00Z",
  "url": "url.com/test"
}
```

MESSAGE

```json
{
  "id": "d2e3293c-2bfc-4fc7-bf12-49f07c877b91",
  "chatId": "76d2e3293c-2bfc-4fc7-bf12-49f07c877b997",
  "content": "Olá, como você está?",
  "timestamp": "2023-07-05T10:30:00Z",
  "sender": "1235678910-2bfc-4fc7-bf12-49f07c877b997"
}
```
