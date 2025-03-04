# Otto the discord-botto
A motivational Discord bot

## What does the bot do?
- Generate and display inspirational and philosophical quotes
- Display encouraging messages
- Greet user in various languages

## Pre-requisites
There are a few things that are required and set up before the bot can be used:
- Have Python 3.8 or higher installed
- Install `requirements.txt`
  - `pip install -r requirements.txt`
- Discord server to invite the Discord bot
- Discord API token 
  - Obtained via [Discord Developer Portal](https://discord.com/developers/) by creating Discord app (bot)
- Create a `.env` file and store your Discord app token like so `TOKEN=[your discord app token]`
- Invite the bot to your Discord server
  
## Get Started
- Use `python main.py` on the CLI to start the bot instance
- Start typing `/` to view the commmands to begin interacting with the bot
  - e.g. `/help`

## Bug stories
### The quotes weren't quoting
After refactoring my codebase such that it was not dependent on Replit and implementing slash commands, I discovered that I was unable to call functions to generate quotes. Despite converting my fetch function into an async function, the bot was unable to provide a response. 

I tested my suspicion that the reponse could be timing out by using `interaction.response.defer(thinking=True)`, and `interaction.followup.send(to_send)` instead of `interaction.response.send_message()`.
  - A followup message via `Interaction.followup` must be sent to make this thinking state from `.defer(thinking=True)` go away.

  ```
  await interaction.response.defer(thinking=True)
  quote = await get_quote()
  await interaction.followup.send(quote)
  ```

My theory proved to be correct, and upon further research I learned from the Discord API docs that response to an interaction must be made within 3 seconds of receiving the event. If the 3 second deadline is exceeded, the interaction will be invalidated.


## Acknowledgements
### API used to generate quotes
- [zenquotes.io](https://zenquotes.io/api/random)
- [stoic-quotes.com](https://stoic-quotes.com/api/quote)
