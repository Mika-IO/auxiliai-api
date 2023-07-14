# provider configuration
provider "aws" {
  region = "us-east-2" # substitua pela região desejada
}

# criação do bucket no S3
resource "aws_s3_bucket" "files-auxiliai" {
  bucket = "files-auxiliai" # substitua pelo nome do bucket desejado
}


# criação da tabela DynamoDB "USERS"
resource "aws_dynamodb_table" "users_table" {
  name         = "USERS"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "email"
  attribute {
    name = "email"
    type = "S"
  }
  tags = {
    Name = "UsersTable"
  }
}


# criação da tabela DynamoDB "CHATS"
resource "aws_dynamodb_table" "chat_table" {
  name         = "CHATS"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  attribute {
    name = "id"
    type = "S"
  }
  tags = {
    Name = "ChatsTable"
  }
}



# criação da tabela DynamoDB "MESSAGES"
resource "aws_dynamodb_table" "message_table" {
  name         = "MESSAGES"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  attribute {
    name = "id"
    type = "S"
  }
  tags = {
    Name = "MessagesTable"
  }
}
