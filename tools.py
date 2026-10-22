
from datetime import datetime
from os import name
import requests

def get_curr_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url,timeout=10)
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
                
            }
        }
    }
]

function_name_mpp = {#we get from llm that konsa function call karna hai, uske liye humne ye dictionary banayi hai ki woh function kaunsa hai, use call karna hai
    "get_curr_time": get_curr_time,
    "get_city_weather": get_city_weather
}