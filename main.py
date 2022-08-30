import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
import lang

client = discord.Client()

grey_words = ['unhappy', 'sorrowful', 'dejected', 'regretful', 'depressed', 'downcast', 'miserable', 'downhearted', 'down', 'despondent', 'despairing', 'disconsolate', 'out of sorts', 'desolate', 'bleak', 'wretched', 'glum', 'gloomy', 'doleful', 'dismal', 'blue', 'melancholy', 'melancholic', 'low-spirited', 'mournful', 'woeful', 'forlorn', 'crestfallen', 'broken-hearted', 'heartbroken', 'inconsolable', 'grief-stricken', 'down in the dumps', 'tragic', 'unfortunate', 'feel awful', 'pitiful', 'pitiable', 'grievous', 'traumatic', 'upsetting', 'depressing', 'distressing', 'dispiriting', 'heartbreaking', 'agonizing', 'distressed', 'distressful', 'regrettable', 'feel sorry', 'deplorable', 'lamentable', 'pathetic', 'shameful', 'disgraceful', 'sad', 'saddened', 'dispirited', 'low', 'heavy-hearted', 'morose', 'weighed down', 'oppressed', 'tearful', 'upset', 'disheartened', 'discouraged', 'daunted', 'pessimistic', 'fed up', 'feel shit']

starter_encouragements = [
  "Hang in there",
  "You'll get through this",
  "Just remember, peaks and troughs"
]

# create separate dictionary for makind edits to command
command_help = {
    ".inspire": "Returns a random quote", 
    ".new_enc": "Add encouragement", 
    ".del_enc": "Remove encouragement", 
    ".list_enc": "Display ALL encouragements", 
    ".respond_enc": "Toggle encouragement Message",
    ".toggle_otto": "Instruct dog to come or go"
    }

# Write Fn to Add/Del otto_talk,  db["hey otto"]
otto_talk = {
    "greet" : {
        "English" : ["How can I help?", "Sup", "Woof!", "Hi there"], 
        "French" : ["Comment puis-je aider ?", "Quoi de neuf ?", "Wouf !", "Coucou"],
        "Spanish" : ["¿ Cómo puedo ayudar ?", "¿ Qué tal ?", "¡ Jau !", "Hola"],
        "Russian" : ["Чем я могу помочь?", "Что нового?", "Гав!", "Привет"],
        "German" : ["Wie kann ich helfen?", "Wie geht's?", "Wuff!", "Grüß dich"],
        "Dutch" : ["Hoe kan ik helfen?", "Hé", "Woef!", "Hallo daar"]
    }, 
    "philosopher" : ["epictetus", "marcus aurelius", "seneca"]
    }

if "respond_enc" not in db.keys():
    db["respond_enc"] = True

if "command help" not in db.keys():
    db["command help"] = {}
else:
    db["command help"] = dict(command_help)

if "encouragements" not in db.keys() or len(db["encouragements"]) == 0:
    db["encouragements"] = list(starter_encouragements)

if "hey otto" not in db.keys() or len(db["hey otto"]) == 0:
    db["hey otto"] = dict(otto_talk)

# otto toggle
if "toggle_otto" not in db.keys():
    db["toggle_otto"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n - " + json_data[0]['a']
    return quote

def get_stoic_quote():
    handle = requests.get("https://stoic-server.herokuapp.com/random")
    json_data = json.loads(handle.text)
    quote = json_data[0]['body'] + '\n - ' + json_data[0]['author'] + ' ({})'.format(json_data[0]['quotesource'])
    return quote

def quote_bystoic(phil):
    handle = requests.get("https://stoic-server.herokuapp.com/search/{}".format(phil))
    total_quotes = len(json.loads(handle.text))
    json_line = json.loads(handle.text)[random.randrange(total_quotes)] 
    quote = json_line['body'] + '\n - ' + json_line['author'] + ' ({})'.format(json_line['quotesource'])
    return quote

def add_encouragements(encouraging_message):
    prep_msg = encouraging_message.split('.')
    out = '. '.join(sentence.strip().capitalize() for sentence in prep_msg)
    db["encouragements"].append(out)

def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements

def display_help():
    out = ''
    for key in command_help:
        if len(out) < 1:
          prep = '+ ' + str(key) + ': ' + str(command_help[key])
        else:
          prep = '\n+ ' + str(key) + ': ' + str(command_help[key])
        out += prep
    return out

def display_enc():
    return '\n'.join(str(i+1) + ' -  ' + db["encouragements"][i] for i in range(len(db["encouragements"])))
    
def hey_otto(): 
    # then, get random message. 
    greet_lang = random.choice(list(db["hey otto"]["greet"]))
    greeting_index = random.randrange(len(db["hey otto"]["greet"][greet_lang]))

    # if message is not in EN, get EN message and orig_message language
    if greet_lang != "English":
        return "{}\nI just said '{}' in {}, if you're at all curious".format(db["hey otto"]["greet"][greet_lang][greeting_index], db["hey otto"]["greet"]["English"][greeting_index], greet_lang)
    return db["hey otto"]["greet"][greet_lang][greeting_index]


@client.event
# When Bot ready, prints User's name
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
# when message is from Users, not Bot itself
async def on_message(message):
    if message.author == client.user:
        return
  
    # Bot command begins '.' Use as Test
    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')

    # Shortcuts
    msg = message.content
    post = message.channel

    # if otto toggle ON
    if db["toggle_otto"]:
        if msg.lower().startswith("what is your name?") or msg.lower().startswith("is your name dog?"):
          await post.send('My name is otto')

    if msg.lower().startswith("how interesting") or msg.lower().startswith("is it really?"):
        await message.channel.send('It is indeed')

    if msg.lower() == "hey otto":
        # run function, returns message, language and translation if message not in EN
        await post.send(hey_otto())

    if msg.lower().startswith("inspire"):
        quote = get_quote()
        await post.send(quote)

    # random quote by philosopher
    if "quote" in msg.lower().split():
        locat = db["hey otto"]["philosopher"]
        if any(phil in msg.lower() for phil in locat):
            stoic = [phil for phil in locat if phil in msg.lower()]
            rando_quote = quote_bystoic(stoic[0])
            await post.send(rando_quote)

    if "stoic" in msg.lower().split():
        await post.send(get_stoic_quote())

    # Encouragement ON
    if db["respond_enc"]:
        if any(word in msg.lower().split() for word in grey_words):
            await post.send(random.choice(db["encouragements"]))

    # Commands
    if msg.startswith('.new_enc'):
        # slice message after command
        encouraging_message = msg.split('.new_enc ',1)[1]
        add_encouragements(encouraging_message)
        await post.send(f"NEW encouragement added.")

    if msg.startswith('.del_enc'):
        encouragements = []
        if "encouragements" in db.keys():
          index = int(msg.split(".del_enc",1)[1])
          # Display_enc shows Enc start at 1, i.e. NOT 0 index
          if index > 0 and index <= len(db["encouragements"]):
            delete_encouragement(index - 1)
            encouragements = list(db["encouragements"])
            await post.send("Changes to Encouragements has been made")
            await post.send(encouragements)
          else:
            await post.send(f'Oh dear, this selection is unavailable. Please choose a value between 1 and {len(db["encouragements"])} next time')

    if msg.startswith(".list_enc"):
        if "encouragements" in db.keys():
          encouragements = db["encouragements"]
        else:
          encouragements = []
        await post.send(encouragements)

    if msg.startswith(".help"):
        await post.send(display_help())

    if msg.startswith(".show_db_keys"):
        key_str = '\n'.join(key for key in db.keys())
        await post.send(key_str)
        await post.send("----- Done -----")

    if msg.startswith(".display_enc"):
        await post.send(display_enc())


    ## Toggles
    if msg.startswith(".respond_enc"):
        value = msg.split(".respond_enc ",1)[1]
        if value.lower() == "true":
            db["respond_enc"] = True
            await post.send("Encouragement Response is ON")
        else:
            db["respond_enc"] = False
            await post.send("Encouragement Response is OFF")

    if msg.startswith(".toggle_otto"):
        value = msg.split(".toggle_otto ",1)[1]
        if value.lower() == "true":
            db["respond_enc"] = True
            await post.send("otto is here!")
        else:
            db["respond_enc"] = False
            await post.send("otto has gone to take a nap")
  
    if msg.startswith(".langf"):
        to_detect = msg.split(".langf ",1)
        await post.send(lang.lang_detect(to_detect[1]))

keep_alive()
client.run(os.environ['TOKEN'])
