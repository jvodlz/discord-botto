import requests
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
URL = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

with open("commands.yaml", "r") as file:
    data = file.read()

commands = yaml.safe_load(data)
headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

# POST command upserts
for cmd in commands:
    response = requests.post(URL, json=cmd, headers=headers)
    cmd_name = cmd["name"]
    print(f">> Creating command: {cmd_name}  [ status: {response.status_code} ]")