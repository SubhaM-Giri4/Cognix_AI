
from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import TOOLS, function_name_mpp
import json

load_dotenv()  #by default looks for .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

MAX_STEPS = 5

#system prompting for behaviour of the agent
# messages.append(
#     {
#         "role": "system",
#         "content": "Act like a very sarcastic assistant and give sarcastic responses in short."
#     }
# )
messages.append(
    {
        "role": "system",
        "content": "give responses in hinglish."
    }
)

while True:

    user_input = input("\nSUBHAM: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    #1st call to llm
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS
        )

        msg = response.choices[0].message

        # even try to print the full response and see the whole response kaise tool milta ki konsa tool call karna hai
        if msg.tool_calls:
            messages.append(msg)

            for tool_call in msg.tool_calls:
                function_name = tool_call.function.name
                func_args = {}

                try:
                    func_args = json.loads(tool_call.function.arguments or "{}")
                    fn = function_name_mpp.get(function_name)

                    if fn is None:
                        raise ValueError("Unknown function: " + function_name)

                    tool_response = fn(**func_args)

                except Exception as e:
                    tool_response = f"Error calling function {function_name}: {str(e)}"

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(tool_response)
                    }
                )

        else:
            messages.append(msg)
            print("Assistant: " + (msg.content or ""))
            break
     
    else:
        fallback = "Sorry, I could not finish this within the step limit."
        messages.append(
            {
                "role": "assistant",
                "content": fallback
            }
        )
        print("Assistant: " + fallback)

#2nd call to llm happens in the next iteration