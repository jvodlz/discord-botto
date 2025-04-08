import os
import pandas as pd
import requests
import regex

from config import WEATHER_API_KEY

country_codes = None
code_country_map = None


async def weather(option: str, *args) -> str:
    global code_country_map
    code_country_map = create_code_country_dict()
    if option == "forecast":
        location = args[0]
        country = args[1] if args[1] is not None else ""

        if regex.match(r"^[\p{L} ,'$$.-]+$", location, regex.IGNORECASE) is None:
            return (
                "Hmm... Something went wrong. Please check your spelling and try again."
            )

        if location.lower() == "antarctica":
            geo_data = (-78.1586, 16.4063, "Antarctica", "AQ")
            return await get_forecast(geo_data)

        geo_data = await get_geodata(location, country)
        if geo_data == (None, None, None, None):
            if country:
                return f"Uh oh! Data for {location}, {country} is unavailable."
            return f"Uh oh! Data for {location} is unavailable."
        return await get_forecast(geo_data)

    elif option == "search":
        country = args[0]
        code = search_country_code(country)
        if code:
            return code
        return f"Uh oh! Unable to find country code for ***{country}***."


def create_country_code_dict() -> dict:
    cwd = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(cwd, "..", "data", "country_codes.csv")
    df = pd.read_csv(data_path)
    clean_countries = df.common_name.str.strip().str.lower()
    data_out = pd.Series(df.iso_alpha_2.values, index=clean_countries).to_dict()
    return data_out


def create_code_country_dict() -> dict:
    cwd = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(cwd, "..", "data", "country_codes.csv")
    df = pd.read_csv(data_path)
    data_out = pd.Series(df.common_name.values, index=df.iso_alpha_2).to_dict()
    return data_out


async def get_geodata(location: str, country: str) -> tuple:
    if country:
        country_code = (
            country if get_country_by_code(country) else search_country_code(country)
        )
    query = f"{location},{country_code}" if country else f"{location}"
    GEO_URL = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=1&appid={WEATHER_API_KEY}"
    response = requests.get(GEO_URL)
    data = response.json()
    if data:
        return data[0]["lat"], data[0]["lon"], data[0]["name"], data[0]["country"]
    return None, None, None, None


def get_weather_icon(weather_id: int, condition: str) -> str:
    icon_map = {
        741: ":fog:",
        762: ":volcano:",
        781: ":cloud_tornado:",
        801: ":white_sun_small_cloud:",
        802: ":partly_sunny:",
        803: ":white_sun_cloud:",
        804: ":cloud:"
    }

    if condition == "Thunderstorm":
        if weather_id in {201, 211, 212}:
            return ":cloud_lightning:"
        return ":thunder_cloud_rain:"
    elif condition == "Drizzle":
        if weather_id in {302, 312, 314}:
            return ":cloud_rain:"
        return ":white_sun_rain_cloud:"
    elif condition == "Rain":
        return ":cloud_rain:"
    elif condition == "Snow":
        if weather_id in {600, 601, 602}:
            return ":snowman2:"
        return ":cloud_snow:"
    elif condition == "Clear":
        return ":sunny:"
    elif condition == "Atmosphere" or condition == "Clouds":
        return icon_map.get(weather_id, "")


def get_temperature_icon(temp: int) -> str:
    if temp <= 0:
        return ":cold_face:"
    elif temp >= 1 or temp <= 10:
        return ":coffee:"
    elif temp >= 11 or temp <= 18:
        return ":leaves:"
    elif temp >= 19 or temp <= 24:
        return ":beach:"
    elif temp >= 25 or temp <= 29:
        return ":melting_face:"
    elif temp >= 30 or temp <= 35:
        return ":hot_face:"
    else:
        return ":fire:"


async def get_forecast(geo_data) -> str:
    lat, lng, location, country_code = geo_data
    WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(WEATHER_URL)
    data = response.json()

    weather_id = int(data["weather"][0]["id"])
    weather_condition = data["weather"][0]["main"]
    description = data["weather"][0]["description"]
    temp = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    cloudiness = data["clouds"]["all"]

    rain = data["rain"]["1h"] if "rain" in data else ""
    snow = data["snow"]["1h"] if "snow" in data else ""

    temperature_icon = get_temperature_icon(feels_like)
    weather_icon = get_weather_icon(weather_id, weather_condition)
    flag = f":flag_{country_code.lower()}:"
    country = code_country_map.get(country_code) or country_code

    #  May not always return an icon for weather condition output
    condition_out = (
        f"{weather_icon} `{description}`" if weather_icon else f"`{description}`"
    )

    out = (
        f"> Current weather in {flag} **{location}**, ***{country}***\n"
        f"***Temperature***: `{temp}°C` ( Feels like {temperature_icon} `{feels_like}°C` )\n"
        f"***Condition***: {condition_out}\n"
        f"***Humidity***: :sweat_drops: `{humidity}%`\n"
        f"***Wind Speed***: :dash: `{wind_speed} m/s`\n"
        f"***Cloudiness***: :cloud: `{cloudiness}%`\n"
    )

    if rain:
        out += f"***Precipitation***: :droplet: `{rain} mm/h`\n"
    if snow:
        out += f"***Snow***: :snowflake: `{snow} mm/h`\n"
    return out


def search_country_code(country: str) -> str:
    global country_codes
    if country_codes is None:
        country_codes = create_country_code_dict()
    return country_codes.get(country.lower(), "")


def get_country_by_code(code: str):
    return code_country_map.get(code.upper(), "")
