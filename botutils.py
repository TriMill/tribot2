import discord

import random
import urllib.parse
import requests

class UserException(Exception):
    pass

COLOR_POLL = discord.Colour.teal()
COLOR_HELP = discord.Colour.green()
COLOR_WEB = discord.Colour.blue()

NUM_EMOJIS = [str(x) + "\uFE0F\u20E3" for x in range(10)]

EIGHTBALL_ANSWERS = [
    "It is certain.", "It is decidedly so.", "Without a doubt.",
    "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
    "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",

    "Reply hazy, try again.", "Ask again later.", "Better not tell you know.",
    "Cannot predict now.", "Concentrate and ask again.",

    "Don't count on it.", "My reply is no.", "My sources say no.",
    "Outlook not so good.", "Very doubtful."
]

def roll_dice(dicestr):
    repl = dicestr.replace("-", "+-")
    dice = dicestr.split("+")
    rolls = []
    for die in dice:
        if len(die) == 0: continue
        sign = 1
        if die[0] == '-':
            die = die[1:]
            sign = -1
        parts = (" " + die).split("d")
        if len(parts) == 1:
            try: rolls.append(int(parts[0][1:])*sign)
            except: raise UserException("Number of sides must be an integer")
        elif len(parts) == 2:
            if parts[0] == " ":
                count = 1
            else:
                try: count = int(parts[0][1:])
                except: raise UserException("Number of dice must be an integer")

            try: sides = int(parts[1])
            except: raise UserException("Number of sides must be an integer")

            if sides <= 0: raise UserException("Number of sides must be positive")
            for _ in range(count):
                rolls.append(sign*random.randrange(1, sides+1))
        else: raise UserException("Invalid dice notation")
    if len(rolls) == 0:
        raise UserException("No dice specified")
    return rolls


def wikipedia(query):
    s = urllib.parse.quote(query)
    link = f"https://en.wikipedia.org/wiki/Special:Search?search={s}&go=Go"
    return link

def xkcd(query):
    if len(query) > 0:
        try:
            query = str(int(query))
        except Exception as e:
            raise UserException("Invalid comic number")
    response = requests.get(f"https://xkcd.com/{query}/info.0.json")
    if not response.ok:
        raise UserException("Comic not found")

    try:
        response = response.json()
    except Exception as e:
        raise UserException("Comic not found")

    return response

imgflip_templates = {
    "drake": 181913649,
    "twobuttons": 87743020,
    "changemind": 129242436,
    "exitramp": 124822590,
    "draw25": 217743513,
    "button": 119139145,
    "bernie": 222403160,
    "handshake": 135256802,
    "samepicture": 180190441,
    "thisisfine": 55311130,
    "truthscroll": 123999232,
    "fanvsenjoyer": 280253821,
}

def imgflip(query, login):
    parts = query.split(";")
    if len(parts) == 0:
        raise UserException("No template specified. See `;help imgflip` for a list.")
    elif len(parts) == 1:
        raise UserException("At least one text required.")
    if parts[0] not in imgflip_templates:
        raise UserException("Invalid template name. See `;help imgflip` for a list.")

    tid = imgflip_templates[parts[0]]
    parts = parts[1:]

    params = {"template_id": tid, "username": login[0], "password": login[1]}
    for i, t in enumerate(parts):
        params["text" + str(i)] = t
    response = requests.post("https://api.imgflip.com/caption_image", params=params)
    if not response.ok:
        raise UserException("Error generating meme.")
    response = response.json()
    if "success" not in response or response["success"] != True:
        raise UserException("Error generating meme.")
    return response["data"]
