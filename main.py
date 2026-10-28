import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("API key not found!")
        
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages=[
        {"role": "system", "content": system_prompt},
        { "role": "user", "content": args.user_prompt}
    ]

    for i in range(20):
        response = client.chat.completions.create(
        model="deepseek/deepseek-v4.1-flash-1017",
        messages=messages,
        tools=available_functions
        )

        if response.usage == None:
            raise RuntimeError("API request failed!")

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        print(response.choices[0].message.content)
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                # print(tool_call)
                result_message = call_function(tool_call)
                if not result_message['content']:
                    raise Exception("Tool call failed")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else: break


if __name__ == "__main__":
    main()
