import requests
import yaml

from config import TOKEN, APPLICATION_ID

URL = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

with open("commands/commands.yaml", "r") as file:
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