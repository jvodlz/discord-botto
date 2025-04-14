import requests
import json


async def inspire(option: str) -> str:
    if option == "random":
        return await get_quote()
    elif option == "stoic":
        return await get_stoic_quote()


async def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    data = json.loads(response.text)
    quote = f"*{clean_quote(data[0]['q'])}*\n— **{data[0]['a']}**"
    return quote


async def get_stoic_quote():
    response = requests.get("https://stoic-quotes.com/api/quote")
    data = json.loads(response.text)
    quote = f"*{clean_quote(data['text'])}*\n— **{data['author']}**"
    return quote


def clean_quote(quote):
    return quote.strip()
