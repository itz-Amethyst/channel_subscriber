# File path to store the page token
import json
import os

PAGE_TOKEN_FILE = "log/page_token.json"

# Function to read the stored page token
def read_page_token():
    if os.path.exists(PAGE_TOKEN_FILE):
        with open(PAGE_TOKEN_FILE, "r") as file:
            data = json.load(file)
            return data.get("nextPageToken", None)
    return None

# Function to write the page token
def write_page_token(token):
    with open(PAGE_TOKEN_FILE, "w") as file:
        json.dump({"nextPageToken": token}, file)