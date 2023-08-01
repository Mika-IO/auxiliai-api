import openai

# Initialize the API key
openai.api_key = "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"


def generate_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        max_tokens=1024,
        temperature=0.5,
    )
    return response.choices[0].message.content, response.usage


def format_to_openai_messages(messages):
    result_array = []
    for message in messages:
        if message["sender"] == "system":
            role = "system"
        else:
            role = "user"
        if message["is_file_message"]:
            role_content_message = {
                "role": role,
                "content": message["file_text"],
            }
            result_array.append(role_content_message)
        else:
            role_content_message = {
                "role": role,
                "content": message["content"],
            }
            result_array.append(role_content_message)
    print[result_array]
    return result_array
