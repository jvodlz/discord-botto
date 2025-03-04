import discord
from discord.ext import commands
import os
import requests
import json
import random
# from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='/', intents=intents)

"""
Initial Responses
"""
grey_words = {
    'unhappy', 'sorrowful', 'dejected', 'regretful', 'depressed', 'downcast',
    'miserable', 'downhearted', 'down', 'despondent', 'despairing',
    'disconsolate', 'out of sorts', 'desolate', 'bleak', 'wretched', 'glum',
    'gloomy', 'doleful', 'dismal', 'blue', 'melancholy', 'melancholic',
    'low-spirited', 'mournful', 'woeful', 'forlorn', 'crestfallen',
    'broken-hearted', 'heartbroken', 'inconsolable', 'grief-stricken',
    'down in the dumps', 'tragic', 'unfortunate', 'feel awful', 'pitiful',
    'pitiable', 'grievous', 'traumatic', 'upsetting', 'depressing',
    'distressing', 'dispiriting', 'heartbreaking', 'agonizing', 'distressed',
    'distressful', 'regrettable', 'feel sorry', 'deplorable', 'lamentable',
    'pathetic', 'shameful', 'disgraceful', 'sad', 'saddened', 'dispirited',
    'low', 'heavy-hearted', 'morose', 'weighed down', 'oppressed', 'tearful',
    'upset', 'disheartened', 'discouraged', 'daunted', 'pessimistic', 'fed up',
    'feel shit'
}

encouragements = {
    "Hang in there", "You'll get through this",
    "Just remember, peaks and troughs",
    "You can demand the best, it's not selfish to care for yourself",
    "There there",
    "Remember to breathe; inhale and exhale deeply",
    "Have пряник, it's so scrummy that you'll crack a smile. Or maybe you know it as lebkuchen",
    "Gimme a sec to collect my farts, they are funny right?"
}

# For Development ONLY
command_help = {
    ".new_enc": "Ajouter un encouragement",
    ".del_enc": "Remove encouragement",
    ".list_enc": "Display **ALL** encouragements",
    ".new_greet": 'Add new greeting. English|How can I help?,Sup,Woof!,Hi there',
    ".del_greet_lang": "Remove language greeting",
    ".list_greet": "Display **ALL** greetings"
}

# Write Fn to Add/Del otto_talk
otto_talk = {
    "greet": {
        "English": ["How can I help?", "Sup", "Woof!", "Hi there"],
        "Bosnian": ["Kako mogu pomoći?", "Šta ima?", "Av!", "Zdravo"],
        "French": ["Comment puis-je aider ?", "Quoi de neuf ?", "Wouf !", "Coucou"],
        "Spanish": ["¿ Cómo puedo ayudar ?", "¿ Qué tal ?", "¡ Jau !", "Hola"],
        "Russian": ["Чем я могу помочь?", "Что нового?", "Гав!", "Привет"],
        "German": ["Wie kann ich helfen?", "Wie geht's?", "Wuff!", "Grüß dich"],
        "Dutch": ["Hoe kan ik helfen?", "Hé", "Woef!", "Hallo daar"]
    },
    "philosopher": {"epictetus", "marcus aurelius", "seneca"}
}

toggles = {
    "respond_enc": True,
    "otto": True
}


"""
Development Functions
"""
async def add_encouragements(message, post):
    prep_msg = message.split('.')
    out = '. '.join(sentence.strip().capitalize() for sentence in prep_msg)
    encouragements.add(out)
    await post.send(f"**NEW encouragement** added: ***{out}***\nHopefully you got the spelling right")


async def delete_encouragement(message, post):
    try:
        encouragements.remove(message)
    except KeyError:
        await post.send("Oopsie daisies!?!? The **encouragement** you want to remove does not exist. Please check your spelling.")
    else:
        await post.send(f"***{message}*** has been removed")


def display_help():
    return '\n'.join(f'+ **{key}**:   *{command_help[key]}*' for key in command_help)


def display_enc():
    return '\n'.join(f'*{i+1}*  **{message}**' for i, message in enumerate(encouragements))


async def add_greeting(lang, message, post):
    clean_lang = lang.lower().strip().capitalize()
    clean_msg = [phrase.capitalize() for phrase in message.lower().split(",")]
    otto_talk['greet'][clean_lang] = clean_msg
    if clean_lang not in otto_talk['greet']:
        await post.send(f"{clean_lang}: {clean_msg} has been added")
    else:
        await post.send(f"**{clean_lang}** has been updated with: *{clean_msg}*")


async def delete_greeting_lang(lang, post):
    clean_lang = lang.lower().capitalize()
    if clean_lang in otto_talk['greet']:
        removed = otto_talk['greet'].pop(clean_lang)
        await post.send(f"**{clean_lang}**: *{removed}* has been removed")
    else:
        await post.send(f"***{clean_lang}*** greetings do not exist")

def display_greet():
    return '\n'.join(f"*{i}* **{lang}**: {greetings}" for i, (lang, greetings) in enumerate(otto_talk['greet'].items(), start=1))


"""
Helpers
"""
def otto_greet():
    lang = random.choice(list(otto_talk['greet'].keys()))
    greet_index = random.randrange(len(otto_talk['greet'][lang]))
    out = otto_talk['greet'][lang][greet_index]
    if lang != "English":
        return out + f"\nI just said ***'{otto_talk['greet']['English'][greet_index]}'*** in **{lang}**, if you're at all curious"
    return out


async def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = f"*{json_data[0]['q']}*\n— **{json_data[0]['a']}**"
    return quote


async def get_stoic_quote():
    handle = requests.get("https://stoic-quotes.com/api/quote")
    json_data = json.loads(handle.text)
    quote = f"*{json_data['text']}*\n— **{json_data['author']}**"
    return quote


"""
Commands
"""
@bot.event
# When Bot ready, prints User's name
async def on_ready():
    await bot.tree.sync()
    print('We have logged in as {0.user}'.format(bot))


@bot.tree.command(name='inspire', description='Get an inspirational quote')
async def inspire(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    quote = await get_quote()
    await interaction.followup.send(quote)


@bot.tree.command(name='stoic', description='Returns a stoic quote')
async def stoic(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    quote = await get_stoic_quote()
    await interaction.followup.send(quote)


@bot.tree.command(name='hello', description='Say hello')
async def hello(interaction: discord.Interaction):
    lang = random.choice(list(otto_talk['greet'].keys()))
    out = otto_talk['greet'][lang][3]
    await interaction.response.send_message(out)


@bot.tree.command(name='toggle-otto', description='Instruct Hond to come or go')
async def toggle_otto(interaction: discord.Interaction):
    toggles['otto'] = not toggles['otto']

    if toggles['otto']:
        await interaction.response.send_message("otto is here!")
    else:
        await interaction.response.send_message("otto has gone to take a nap")


@bot.tree.command(name='encouragement-toggle', description='Toggle encouragement Message')
async def enc_toggle(interaction: discord.Interaction):
    toggles['respond_enc'] = not toggles['respond_enc']
    out = "ON" if toggles['respond_enc'] else "OFF"
    await interaction.response.send_message(f'**Encouragement** Message is now ***{out}***')


@bot.event
# when message is from Users, not Bot itself
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    # Shortcuts
    msg = message.content
    post = message.channel

    if msg.lower().startswith("how interesting") or msg.lower().startswith(
            "is it really?"):
        await message.channel.send('It is indeed')

    if msg.lower() == "hey otto" and toggles['otto']:
        await post.send(otto_greet())

    # Grey words handling
    if toggles['respond_enc']:
        words = msg.lower().split()
        for i, word in enumerate(words):
            if word in grey_words:
                if i > 0 and words[i-1] == "not":
                    continue
                else:
                    await post.send(random.choice(list(encouragements)))
                    break

    """
    Development Function Command Calls
    """
    if msg.startswith(".new_enc"):
        try:
            encouraging_message = msg.split('.new_enc ', maxsplit=2)[1]
        except IndexError:
            await post.send("Hmm... Did you forget to mention the new **Encouragement**?")
        else:
            await add_encouragements(encouraging_message, post)

    elif msg.startswith(".del_enc"):
        parts = msg.split(".del_enc", maxsplit=2)
        if len(parts) > 1:
            enc_for_removal = parts[1].strip()
            await delete_encouragement(enc_for_removal, post)
        else:
            await post.send("Hmm... Did you forget to mention the **Encouragement** for removal?")

    elif msg.startswith(".list_enc"):
        out = "\n".join(boost for boost in encouragements)
        await post.send(out)

    elif msg.startswith(".new_greet"):
        try:
            entry = msg.split('.new_greet ', maxsplit=2)[1]
            lang, greeting = entry.split("|")

        except IndexError:
            await post.send("Hmm... Did you forget to mention the new **Greeting**?")
        except ValueError:
            await post.send("Hmm... Maybe check the formatting real quick. language|a,b,c,d")
        else:
            await add_greeting(lang, greeting, post)

    elif msg.startswith(".del_greet_lang"):
        parts = msg.split(".del_greet_lang", maxsplit=2)
        if len(parts) > 1:
            lang_removal = parts[1].strip()
            await delete_greeting_lang(lang_removal, post)
        else:
            await post.send("Hmm... Did you forget to mention the **Greeting Language** for removal?")

    elif msg.startswith(".list_greet"):
        await post.send(display_greet())

    elif msg.startswith(".help"):
        await post.send(display_help())

    elif msg.startswith(".display_enc"):
        await post.send(display_enc())

# keep_alive()
bot.run(os.getenv('TOKEN'))