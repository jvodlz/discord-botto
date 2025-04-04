from flask import Flask, jsonify, request
from discord_interactions import verify_key_decorator
from asgiref.wsgi import WsgiToAsgi
from mangum import Mangum
import httpx
import logging

from config import PUBLIC_KEY, APPLICATION_ID
from commands import greet, inspire, weather, timestamp

logger = logging.getLogger()
logger.setLevel(logging.INFO)


app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)
logger.info("Create Flask app and Lambda Handler")


@app.route("/", methods=["POST"])
async def interactions():
    raw_request = request.json
    return await interact(raw_request)


def get_cmd(data):
    return data["name"]


def get_subcmd(data):
    return data["options"][0]["name"]


def get_subcmd_value_at_index(data, index):
    try:
        return data["options"][0]["options"][index]["value"]
    except IndexError:
        return None


def handle_timestamp(data):
    date = data["options"][0]["value"]
    time = data["options"][1]["value"]
    return timestamp(date, time)


async def handle_weather(data):
    sub_cmd_group = data["options"][0]["name"]
    sub_cmd_group_options = data["options"][0]
    message_content = (
        "Uh oh! An error occurred with the weather command. Please try again later."
    )

    if sub_cmd_group == "info":
        sub_command = get_subcmd(sub_cmd_group_options)
        if sub_command == "forecast":
            location = get_subcmd_value_at_index(sub_cmd_group_options, 0)
            country = get_subcmd_value_at_index(sub_cmd_group_options, 1)
            message_content = await weather("forecast", location, country)

        elif sub_command == "search":
            country = get_subcmd_value_at_index(sub_cmd_group_options, 0)
            message_content = await weather("search", country)
    return message_content


async def handle_defer_callback(interaction_id, interaction_token):
    URL = f"https://discord.com/api/v10/interactions/{interaction_id}/{interaction_token}/callback"
    deferred_response = {"type": 5}  # DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(URL, json=deferred_response)
            logger.info(
                f">> Deferring interaction  [ status: {response.status_code} ]"
            )
        except httpx.RequestError as e:
            logger.error(
                f">>>> Uh oh! An error occurred while deferring the response:\n{e}"
            )


async def update_original_interaction_reponse(interaction_token, content):
    URL = f"https://discord.com/api/v10/webhooks/{APPLICATION_ID}/{interaction_token}/messages/@original"
    headers = {"Content-Type": "application/json"}
    data = {"content": content}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(URL, json=data, headers=headers)
            response.raise_for_status()
            return True
        except httpx.RequestError as e:
            logger.error(
                f">>>> Hmm... an error occurred while sending interaction response:\n{e}"
            )
            return False


async def process_commands(data):
    command_name = get_cmd(data)
    message_content = "Hmm... an error occurred while sending interaction response"

    if command_name == "hello":
        message_content = greet()

    elif command_name == "inspire":
        sub_command = get_subcmd(data)
        if sub_command == "random":
            message_content = await inspire("random")
        elif sub_command == "stoic":
            message_content = await inspire("stoic")

    elif command_name == "weather":
        message_content = await handle_weather(data)

    elif command_name == "timestamp":
        message_content = handle_timestamp(data)

    return message_content


@verify_key_decorator(PUBLIC_KEY)
async def interact(raw_request):
    response_data = {"type": 1}
    if raw_request["type"] == 1:  # PING
        return jsonify(response_data)

    elif raw_request["type"] == 2:  # APPLICATION_COMMAND
        interaction_id = raw_request["id"]
        interaction_token = raw_request["token"]
        logger.info(">> Deferring interaction callback")
        await handle_defer_callback(interaction_id, interaction_token)

        data = raw_request["data"]
        message_content = await process_commands(data)

        # Interaction Callback Type 4 : Respond to interaction with message
        response_data = {"type": 4, "data": {"content": message_content}}

    logger.info(">> Updating original interaction response")
    if not await update_original_interaction_reponse(
        interaction_token, message_content
    ):
        logger.info(">> Error updating original interaction response")

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
