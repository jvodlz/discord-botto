# Otto the discord-botto
A Swiss Army knife kind of Discord bot, kind of.

The project implements a Python Discord bot that is hosted on AWS Lambda within a Docker Container. The infrastructure is managed using AWS Cloud Development Kit (CDK).

```                                              
  +----------------+        +----------------+       +--------------------+    +---------------------+
  |    Discord     |  HTTP  |                |       |                    |    |                     |
  |  (User Input)  +------->+  API Gateway   +------>+     AWS Lambda     +--->+   CloudWatch Logs   |
  +----------------+        |                |       |                    |    |                     |
                            +----------------+       |  +--------------+  |    +---------------------+
                                                     |  | Docker Image |  |
                                                     |  +--------------+  |
                                                     |                    |
                                                     +---------+----------+
                                                               |
                                                               v
                                                        +-------------+
                                                        |   AWS CDK   |
                                                        +-------------+
```

## What does the bot do?
- Generate inspirational and philosophical quotes
- Get current weather forecast by location and ISO 3166 country code
- Generate Discord timestamps
- Greet users in various languages

## Pre-requisites
There are a few things that are required and set up before the bot can be used:
- Have Python 3.11 or higher installed
- Install `requirements.txt`
  - `pip install -r requirements.txt`
- Discord server to invite the Discord bot
- Discord API token 
  - Obtained via [Discord Developer Portal](https://discord.com/developers/) by creating Discord app (bot)
- Create a `.env` file in the root project directory and store e.g. your Discord app token like so `TOKEN=[your discord app token]`
- Invite the bot to your Discord server
- Configure AWS Credentials
- Ensure [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) is set up

## Environment Variables
Required secrets in `.env` and AWS Lambda:
- `TOKEN` - Discord bot token
- `APPLICATION_ID` - Discord application id
- `PUBLIC_KEY` - Discord public key
- `WEATHER_API_KEY` - [OpenWeather](https://openweathermap.org) API key


## Registering Commands
The bot must have application commands (slash commands) registered with Discord.

Run `register_commands` from the `src` directory
```
cd src
python -m commands.register_commands
```

## Deploy to AWS Lambda
Bootstrap the CDK
- `cdk bootstrap`

Then, deploy
- `cdk deploy`

## Data
The data used for this project were publicly sourced and were cleaned/transformed for this project. 

### Country Codes
- `iso_alpha` refers to the ISO 3166-1 alpha-2 country code (249 officially assigned)
- `iso_currency_country_name` refers to the country name used in ISO 4217 currency codes
- `common_name` refers to the name a country is commonly referred to

> Countries were renamed to their commonly known names to allow for better usability 

#### Some examples of renaming
- Bolivia (Plurinational State of) `->` **Bolivia**
- Cocos (Keeling) Islands `->` **Cocos Islands**
- Congo `->` **Congo-Brazzaville**
- Democratic Republic of the Congo `->` **Congo-Kinshasa**
- Lao People's Democratic Republic `->` **Laos**
- Republic of Korea `->` **South Korea**
- Svalbard and Jan Mayen Islands -> **Svalbard and Jan Mayen**
- Syrian Arab Republic `->` **Syria**
- United States of America `->` **United States**
- Viet Nam `->` **Vietnam**

#### Special cases for `common_name` (Spelling)
- Åland Islands
- Côte d'Ivoire
- Curaçao

### Time Zones
- `zone_name` refers to the TZ identifier from the [tz database](https://en.wikipedia.org/wiki/Tz_database)

#### Unlisted tzdata
- **BV** - *Bouvet Island*
- **HM** - *Heard Island and McDonald Islands*
- **EH** - *Western Sahara*

## Security
### Discord Interaction Requests
User interactions with the bot requires validation using 
- `X-Signature-Ed25519` as a signature
- `X-Signature-Timestamp` as a timestamp

## Acknowledgements
### API
- [zenquotes.io](https://zenquotes.io/api/random)
- [stoic-quotes.com](https://stoic-quotes.com/api/quote)
- [OpenWeather](https://openweathermap.org)

### Data
- [Country Codes](https://github.com/datasets/country-codes/tree/main/data)
- [Time Zones](https://timezonedb.com/download)