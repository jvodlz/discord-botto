from flask import Flask, jsonify, request
from discord_interactions import verify_key_decorator
from asgiref.wsgi import WsgiToAsgi
from mangum import Mangum

from config import PUBLIC_KEY
from commands import greet, inspire


app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)


@app.route("/", methods=["POST"])
async def interactions():
    raw_request = request.json
    # Debug logging
    print(f"Request: {raw_request}")
    return await interact(raw_request)


# @verify_key_decorator(PUBLIC_KEY)
async def interact(raw_request):
    response_data = {"type": 1}
    if raw_request["type"] == 1:  # PING
        return jsonify(response_data)

    elif raw_request["type"] == 2:  # APPLICATION_COMMAND
        data = raw_request["data"]
        command_name = data["name"]

        if command_name == "hello":
            message_content = greet()
        elif command_name == "inspire":
            sub_command = data["options"][0]["name"]
            if sub_command == "random":
                message_content = await inspire("random")
            elif sub_command == "stoic":
                message_content = await inspire("stoic")

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