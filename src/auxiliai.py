import requests

API_KEY = "ushdkjhshgd"
OPEN_AI_BASE_URL = "https://api.openai.com"


def complete(
    prompt: str, question: str, language: str = "pt", context: list = []
) -> str:
    prompt = get_prompt(context, question, language)
    url = f"{OPEN_AI_BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {API_KEY}",
    }

    messages = []
    messages += context
    messages.append({"role": "user", "content": prompt})
    print("messages", messages)

    # CHAMADA
    data = {"model": "gpt-3.5-turbo", "messages": messages, "n": 1, "max_tokens": 120}
    response = requests.post(url, headers=headers, json=data)

    print("Response", response.json())
    completion = response.json()["choices"][0]["message"]["content"]
    messages.append({"role": "system", "content": completion})
    return completion


def detect_language(text: str) -> str:
    url = f"{OPEN_AI_BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": f"What is the language of the text: {text} among the 3 options: Portuguese, English or Spanish. Answer that way pt, en or es?",
            }
        ],
        "n": 1,
        "max_tokens": 2,
    }

    response = requests.post(url, headers=headers, json=data)
    completion = response.json()["choices"][0]["message"]["content"]

    if completion == "es":
        return "es"
    elif completion == "pt":
        return "pt"
    return "en"


def get_prompt(context: str, question: str, language: str) -> str:
    if language == "pt":
        prompt = f"""
        Baseado nesse contexto:
        {context}
        Responda essa pergunta,
        {question}
        """
    return prompt
