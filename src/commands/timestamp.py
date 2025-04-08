import os
import pandas as pd
import csv
from datetime import datetime
from zoneinfo import ZoneInfo


country_code_map = None
code_tz_map = None
timezone_set = set()


def timestamp(option: str, *args) -> str:
    if option == "search":
        value = args[0]
        #  code -> tz
        if len(value) == 2:
            out = (
                search_timezones(value)
                or " undefined. Please use a valid input e.g. ***NZ***"
            )
            return f"> The timezone(s) for **{value}** is{out}"
        # country -> code
        else:
            prep = f"`{search_country_code(value)}`" if search_country_code(value) else ""
            out = (
                prep
                or "undefined. Please check your spelling and try again"
            )
            return f"> The country code for **{value}** is {out}"

    elif option == "create":
        date_str, time_str, tz_str = args

        if not validate_date(date_str):
            return "Uh oh! Invalid date format. Please check that the date is in ***DD/MM/YYYY***"
        elif not validate_time(time_str):
            return "Uh oh! Invalid time format. Please check that the time is **24-Hour** format ( e.g. ***14:48*** )"

        return get_timestamps(date_str, time_str, tz_str)


def create_code_timezone_dict() -> dict:
    cwd = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(cwd, "..", "data", "tzdata.csv")
    df = pd.read_csv(data_path)
    data_out = df.groupby("country_code")["zone_name"].agg(set).to_dict()
    return data_out


def create_country_code_dict() -> dict:
    cwd = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(cwd, "..", "data", "country_codes.csv")
    df = pd.read_csv(data_path)
    clean_countries = df.common_name.str.strip().str.lower()
    data_out = pd.Series(df.iso_alpha_2.values, index=clean_countries).to_dict()
    return data_out


def create_tz_set() -> set:
    cwd = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(cwd, "..", "data", "tzdata.csv")
    with open(data_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # skip headers
        data_out = {row[0].lower() for row in reader}
        return data_out


def search_timezones(country_code: str) -> str:
    global code_tz_map
    code_tz_map = create_code_timezone_dict()
    if code_tz_map is None:
        code_tz_map = create_code_timezone_dict()

    timezones = code_tz_map.get(country_code.upper())
    if timezones:
        return ":\n" + "`" + "\n".join(timezones) + "`"
    return ""


def search_country_code(country: str) -> str:
    global code_country_map
    country_code_map = create_country_code_dict()
    if country_code_map is None:
        country_code_map = create_country_code_dict()
    return country_code_map.get(country.lower(), "")


def validate_date(date_str):
    try:
        day, month, year = map(int, date_str.split("/"))
        datetime(year, month, day)
        return True
    except ValueError:
        return False


def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def validate_timezone(tz_str):
    global timezone_set
    if not timezone_set:
        timezone_set = create_tz_set()
    return tz_str.lower() in timezone_set


def get_timestamps(date_str: str, time_str: str, tz_str: str) -> str:
    datetime_str = f"{date_str} {time_str}"
    datetime_format = "%d/%m/%Y %H:%M"
    timestamp = "-2146908600"  # 21/12/0001 00:00

    tz_out = tz_str
    out = f"> ***{tz_str}*** was used to generate the timestamp"
    if not validate_timezone(tz_str):
        tz_out = "Etc/UTC"
        out = f"> Hmm... ***{tz_str}*** is not valid or does not exist.\n> **Etc/UTC** was used as default to generate the timestamp"

    try:
        naive_datetime = datetime.strptime(datetime_str, datetime_format)
        local_datetime = naive_datetime.replace(tzinfo=ZoneInfo(tz_out))
        timestamp = int(local_datetime.timestamp())
    except ValueError:
        return "Hmm... An error occurred while generating a timestamp.\nPlease check the spelling and values you entered"
    return (
        f"{out}\n\n"
        f"`<t:{timestamp}:F>`  <t:{timestamp}:F>\n"
        f"`<t:{timestamp}:f>`  <t:{timestamp}:f>\n\n"
        f"`<t:{timestamp}:D>`  <t:{timestamp}:D>\n"
        f"`<t:{timestamp}:d>`  <t:{timestamp}:d>\n\n"
        f"`<t:{timestamp}:t>`  <t:{timestamp}:t>\n"
        f"`<t:{timestamp}:R>`  <t:{timestamp}:R>\n"
    )
