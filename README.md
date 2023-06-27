# discord-botto
Simple inspirational Discord bot using API. This is an ongoing project.

## What does the bot do?
- Generate and display inspirational quotes
- Display encouraging messages
- Add/Remove your own encouraging messages
- Greet user in various languages

## Pre-requisites
There are a few things that are required and set up before the bot can be used:
- Discord API token 
  - Obtained via [Discord Developer Portal](https://discord.com/developers/)
- Replit account 
  - The original bot was made on Replit and made use of their Environment Variables Storage (**Secrets**) to contain API keys and Database System (referenced as ```db["key_name"]```)
- Uptimer Robot account
  - This uptime monitoring service helps to keep the bot running
  
  ## Important command to help get you started
  ``` .help```
  - Displays the list of commands
  
  ## API used to generate quotes
  - [zenquotes.io](https://zenquotes.io/api/random)
  - [~~stoic-api.herokuapp.com~~](https://stoic-api.herokuapp.com) (No longer available)
