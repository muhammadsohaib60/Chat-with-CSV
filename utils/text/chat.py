from openai import OpenAI
from prompts import GENERATE_DEFAULT_PROMPT, custom_system_prompt
import os


def chat(inputText: str, history: list, operationType: str, length_summary: int, key: str):
    response = "Empty"
    user_input = inputText

    client = OpenAI(api_key=key)
    os.environ["OPENAI_API_KEY"] = key

    if (
        operationType == "generate"
    ):

        user_input = inputText
        default_prompt = GENERATE_DEFAULT_PROMPT

        if operationType == "generate":
            user_input = inputText
            if custom_system_prompt is not None:
                default_prompt = custom_system_prompt
            else:
                default_prompt = GENERATE_DEFAULT_PROMPT

        # Consider only the last 50 messages in history
        limited_history = history[-50:] if len(history) > 50 else history

        # Include history in messages
        messages = [{"role": "system", "content": default_prompt}]
        messages.extend([{"role": "user", "content": msg}
                        for msg in limited_history])
        messages.append({"role": "user", "content": user_input.strip()})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response = response.choices[0].message.content
        print("response:", response)
    return response
