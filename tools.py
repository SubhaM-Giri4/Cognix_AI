
from datetime import datetime
from os import name
from Utilities.utilities import log
import requests
import json

def get_curr_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url,timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text

TOOLS = [
    {
        "type":"function",
        "function": {
            "name": "get_curr_time",
            "description": "Get the current date and time in the format YYYY-MM-DD HH:MM:SS",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
    {
        "type":"function",
        "function": {
            "name": "get_city_weather",
            "description": "Get the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get the weather for."
                    }
                },
                "required": ["city"]
                
            }
        }
    }
]

function_name_mpp = {#we get from llm that konsa function call karna hai, uske liye humne ye dictionary banayi hai ki woh function kaunsa hai, use call karna hai
    "get_curr_time": get_curr_time,
    "get_city_weather": get_city_weather
}

def run_tool(tool_call):

    function_name = tool_call.function.name
    func_args = {}

    try:
        func_args = json.loads(tool_call.function.arguments or "{}")
        fn = function_name_mpp.get(function_name)

        log(f"Calling function: {function_name} with arguments: {func_args}")

        if fn is None:
            raise ValueError("Unknown function: " + function_name)

        tool_response = fn(**func_args)

    except Exception as e:
        tool_response = f"Error calling function {function_name}: {str(e)}"

    log(f"Tool result: {tool_response}")
    return str(tool_response)
