import os

def log (text):
    if os.getenv("DEBUG") == "True":
        print(text)