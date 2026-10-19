
from datetime import datetime
from os import name


def get_curr_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    }
]

function_name_mpp = {#we get from llm that konsa function call karna hai, uske liye humne ye dictionary banayi hai ki woh function kaunsa hai, use call karna hai
    "get_curr_time": get_curr_time,
}