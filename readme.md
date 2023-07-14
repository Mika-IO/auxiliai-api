# Auxiliai

A GPT tool to analize PDF documents

#### TODO

- Subir arquivo pro bucket
- No service create-message integrar com open AI
- Melhorar a solucao de permissoes

#### Getting Started

```shell
  # Set up a virtual environment:

  python3 -m venv virtualenv

  # Activate the environment:

  source virtualenv/bin/activate

  # Install the dependencies:

  pip install -r requirements.txt

  # Run the API locally:

  chalice local
```

#### AWS Resources

- Lambda
- S3
- DynamoDB
- JWT

```shell
  # Init infra:
  terraform init

  # Create infra:
  terraform apply

  # Destroy infra:
  terraform destroy
```

#### Endpoits

- POST -> SignUp
- POST -> SignIn
- POST -> Chat
- POST -> Message
- GET -> Chats
- GET -> Messages
- DELETE -> Chat

#### Models

ACCOUNT USERS

```json
{
  "id": "1235678910-2bfc-4fc7-bf12-49f07c877b997",
  "email": "mikaiodev@gmail.com",
  "role": "admin",
  "admin_id": "1235678910-2bfc-4fc7-bf12-49f07c877b997",
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

MESSAGE

```json
{
  "id": "d2e3293c-2bfc-4fc7-bf12-49f07c877b91",
  "chatId": "76d2e3293c-2bfc-4fc7-bf12-49f07c877b997",
  "owner_id": "1235678910-2bfc-4fc7-bf12-49f07c877b997",
  "sender": "user",
  "content": "Olá, como você está?",
  "file_url": "",
  "timestamp": "2023-07-05T10:30:00Z"
}
```
