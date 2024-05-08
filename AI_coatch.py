import requests
import json
import os
import re

openai_api_key = os.environ.get("apikey")


def generate_prompt(prompt):
    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in environment variables.")

    instruction = "Generate a response in HTML format with dark humor"
    if prompt:
        prompt = prompt + instruction
    else:
        prompt = "Generate a response in HTML format without HTML tag, a non image meme"

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "a non image meme, no explanation, give strictly code, "
                           "funny and dark title"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        sentence = response.json()['choices'][0]['message']['content']
        exclude_words = ["```html", "```"]

        pattern = '|'.join(map(re.escape, exclude_words))
        response1 = re.sub(pattern, '', sentence, flags=re.IGNORECASE)
        return response1
    else:
        print("Error:", response.status_code, response.text)
