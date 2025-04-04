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

# Environment Variables
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
### Country Codes Data
The Country Codes were sourced from [SimpleMaps](https://simplemaps.com/data/world-cities). The data was cleaned and transformed for this project. This data is licensed under the Creative Commons Attribution 4.0 International License.