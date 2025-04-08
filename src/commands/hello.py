import random

greetings = {
    "English": ["How can I help?", "Sup", "Woof!", "Hi there"],
    "Bosnian": ["Kako mogu pomoći?", "Šta ima?", "Av!", "Zdravo"],
    "French": ["Comment puis-je aider ?", "Quoi de neuf ?", "Wouf !", "Coucou"],
    "Spanish": ["¿ Cómo puedo ayudar ?", "¿ Qué tal ?", "¡ Jau !", "Hola"],
    "Russian": ["Чем я могу помочь?", "Что нового?", "Гав!", "Привет"],
    "German": ["Wie kann ich helfen?", "Wie geht's?", "Wuff!", "Grüß dich"],
    "Dutch": ["Hoe kan ik helfen?", "Hé", "Woef!", "Hallo daar"],
}


def greet():
    lang = random.choice(list(greetings.keys()))
    greet_index = random.randrange(len(greetings[lang]))
    out = greetings[lang][greet_index]
    if lang != "English":
        return (
            out
            + f"\nI just said ***'{greetings['English'][greet_index]}'*** in **{lang}**, if you're at all curious"
        )
    return out
