import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("apikey")
)

load_dotenv()


def generate_prompt(prompt, model="text-davinci-002", max_tokens=1024, temperature=0.7):

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt
    )
    return response.choices[0].text
