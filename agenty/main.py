import argparse
import json
import os
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)

from functions.call_function import available_functions, call_function
from prompt import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None:
    raise RuntimeError("No api key")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def send_request_to_api_with_tools(
    client: OpenAI, message: list[dict[str, str]], available_functions
) -> ChatCompletion:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=cast(list[ChatCompletionMessageParam], message),
        tools=cast(list[ChatCompletionToolParam], available_functions),
    )
    return response


def build_message(user_prompt: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": user_prompt,
        },
    ]


def run_agent_mode(
    starting_prompt: list[dict[str, str]], limit=20, verbose=False
) -> str:
    messages = starting_prompt
    message_on_failure = ""

    for _ in range(limit):
        response = send_request_to_api_with_tools(client, messages, available_functions)

        if response.usage == None:
            raise RuntimeError("No response")

        if verbose:
            print(f"User prompt: {starting_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        message_on_failure = response
        messages.append(message.model_dump())

        if not message.tool_calls:
            return message.content or ""

        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                raise RuntimeError(f"Unsupported tool call type: {tool_call.type}")

            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")

            result_message = call_function(tool_call)
            messages.append(result_message)

            if len(result_message["content"]) == "":
                raise RuntimeError("No response from model")

            if verbose:
                print(f"-> {result_message['content']}")

    return f"Iteration limit exceeded, last message: {message_on_failure}"


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--limit", type=int, help="Limit agent iterations")

    args = parser.parse_args()

    messages = build_message(args.user_prompt)

    limit = args.limit or 20

    finish_message = run_agent_mode(messages, limit, args.verbose)

    print(finish_message or "")


if __name__ == "__main__":
    main()
