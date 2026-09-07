import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

# Load variables from the .env file.
load_dotenv()

# Get the OpenRouter API key from the environment.
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

# Configure the OpenAI client to use OpenRouter.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():

    # Read the user's prompt from the command line.
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")

    # Optional flag for displaying extra information.
    parser.add_argument("--verbose", action="store_true",help="Enable verbose output")

    args = parser.parse_args()
  
    # The messages list represents the conversation history.
    messages = [
       {"role":"user", "content":args.user_prompt}
    ]

    # Send the conversation to the LLM.
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if response.usage is None:
        raise RuntimeError("Response usage is missing")

    # Show token information only in verbose mode.
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()