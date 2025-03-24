import requests
import json

from config import TOKEN, APPLICATION_ID


URL = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/commands"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

'''
Commands to DELETE
'''
commands = {
    'toggle'
}

del_cmd_len = len(commands)

response = requests.get(URL, headers=headers)
registered_commands = response.json()
# print(json.dumps(registered_commands, indent=2))

# Delete command operation
for del_cmd in commands:
    for cmd in registered_commands:
        if cmd["name"] == del_cmd:
            del_id = cmd["id"]
            del_url = f"{URL}/{del_id}"

            response = requests.delete(del_url, headers=headers)
            print(f"<<<<< Deleting command: {del_cmd}  [ status: {response.status_code} ]")
            del_cmd_length -= 1
            break
    else:
        print("\n" + "***")
        print(f"The command: [{del_cmd}] Does Not Exist")
        print("***" + "\n")

print(f"----- SUCCESSFULLY REMOVED {len(commands) - del_cmd_len} out of {del_cmd_len} -----")