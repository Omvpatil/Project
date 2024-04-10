import os
from dotenv import load_dotenv
import openai

# Load your OpenAI API key from a .env file (recommended for security)
load_dotenv()
OPENAI_API_KEY = os.environ.get("api_key")

openai.api_key = OPENAI_API_KEY


def generate_prompt(prompt, model="text-davinci-003", max_tokens=1024, temperature=0.7):
    """Generates text using the OpenAI API.

  Args:
      prompt: The initial prompt to guide the generation.
      model: The OpenAI model to use for generation (default: "text-davinci-003").
      max_tokens: The maximum number of tokens to generate (default: 1024).
      temperature: The randomness of the generation (0.0 = deterministic, 1.0 = maximal).

  Returns:
      The generated text response from the model.
  """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].text
    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None
