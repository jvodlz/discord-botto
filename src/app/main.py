from flask import Flask, jsonify, request
from discord_interactions import verify_key_decorator
from asgiref.wsgi import WsgiToAsgi
from mangum import Mangum

from config import PUBLIC_KEY
from commands import greet, inspire, weather

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)


@app.route("/", methods=["POST"])
async def interactions():
    raw_request = request.json
    # Debug logging
    print(f"Request: {raw_request}")
    return await interact(raw_request)


def get_cmd(data):
    return data["name"]


def get_sub_cmd(data):
    return data["options"][0]["name"]


def get_value_at_index(data, index):
    try:
        return data["options"][0]["options"][index]["value"]
    except IndexError:
        return None


async def handle_weather(data):
    sub_cmd_group = data["options"][0]["name"]
    sub_cmd_group_options = data["options"][0]
    message_content = (
        "Uh oh! An error occurred with the weather command. Please try again later."
    )

    if sub_cmd_group == "info":
        sub_command = get_sub_cmd(sub_cmd_group_options)
        if sub_command == "forecast":
            location = get_value_at_index(sub_cmd_group_options, 0)
            country = get_value_at_index(sub_cmd_group_options, 1)
            message_content = await weather("forecast", location, country)

        elif sub_command == "search":
            country = get_value_at_index(sub_cmd_group_options, 0)
            message_content = await weather("search", country)
    return message_content


@verify_key_decorator(PUBLIC_KEY)
async def interact(raw_request):
    response_data = {"type": 1}
    if raw_request["type"] == 1:  # PING
        return jsonify(response_data)

    elif raw_request["type"] == 2:  # APPLICATION_COMMAND
        data = raw_request["data"]
        command_name = get_cmd(data)

        if command_name == "hello":
            message_content = greet()

        elif command_name == "inspire":
            sub_command = get_sub_cmd(data)
            if sub_command == "random":
                message_content = await inspire("random")
            elif sub_command == "stoic":
                message_content = await inspire("stoic")

        elif command_name == "weather":
            message_content = await handle_weather(data)

        # Interaction Callback Type 4 : Respond to interaction with message
        response_data = {
            "type": 4,
            "data": {
                "content": message_content,
            },
        }

        return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
