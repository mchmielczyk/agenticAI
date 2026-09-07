import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompt import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function
import json

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("No api key")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    messages=[
            {
                "role": "system",
                "content": system_prompt},
                {"role": "user",
                "content": args.user_prompt,
            }]
    for _ in range(20):
        response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        )
        
        if response.usage == None:
            raise RuntimeError("No response")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message= response.choices[0].message
        messages.append(message)
        if not message.tool_calls:
            print(message.content or "")
            exit(0)
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message= call_function(tool_call)
            messages.append(result_message)
            if len(result_message["content"])=="":
                raise Exception
            if args.verbose:
                print(f"-> {result_message['content']}")

    
    exit(1)


if __name__ == "__main__":
    main()
