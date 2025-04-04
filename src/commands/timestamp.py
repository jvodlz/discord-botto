from datetime import datetime, time


def timestamp(date_str: str, time_str: str) -> str:
    if not validate_date(date_str):
        return "Uh oh! Invalid date format. Please check that the date is in ***DD/MM/YYYY***"
    elif not validate_time(time_str):
        return "Uh oh! Invalid time format. Please check that the time is **24-Hour** format ( e.g. ***14:48*** )"
    return get_timestamps(date_str, time_str)


def validate_date(date_str):
    try:
        day, month, year = map(int, date_str.split("/"))
        datetime(year, month, day)
        return True
    except ValueError:
        return False


def validate_time(time_str):
    try:
        hour, minute = map(int, time_str.split(":"))
        time(hour, minute)
        return True
    except ValueError:
        return False


def get_timestamps(date_str: str, time_str: str) -> str:
    datetime_str = f"{date_str} {time_str}"
    datetime_format = "%d/%m/%Y %H:%M"
    timestamp = "-2146908600"  # 21/12/0001 00:00

    try:
        timestamp = int(datetime.strptime(datetime_str, datetime_format).timestamp())
    except ValueError:
        return "Hmm... An error occurred while parsing the date and time"
    return (
        f"`<t:{timestamp}:F>`  <t:{timestamp}:F>\n"
        f"`<t:{timestamp}:f>`  <t:{timestamp}:f>\n\n"
        f"`<t:{timestamp}:D>`  <t:{timestamp}:D>\n"
        f"`<t:{timestamp}:d>`  <t:{timestamp}:d>\n\n"
        f"`<t:{timestamp}:T>`  <t:{timestamp}:T>\n"
        f"`<t:{timestamp}:t>`  <t:{timestamp}:t>\n"
        f"`<t:{timestamp}:R>`  <t:{timestamp}:R>\n"
    )
