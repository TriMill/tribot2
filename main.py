#!/usr/bin/python3
# https://discord.com/oauth2/authorize?client_id=??????&scope=bot&permissions=8192
import discord
import asyncio
import logging
import datetime
import sys
import os

import commands
import botutils
import cmdhelp

if not os.path.exists("logs"):
    os.mkdir("logs")

timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat().replace(":", "_")
fstr = "%(asctime)s - %(module)s [%(levelname)s] %(message)s"
fmt = logging.Formatter(fmt=fstr)
logging.basicConfig(
        level=logging.INFO,
        format=fstr
)
#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
dated_log = logging.FileHandler("logs/{}.log".format(timestamp), mode="a")
dated_log.setFormatter(fmt)
logging.getLogger().addHandler(dated_log)
latest_log = logging.FileHandler("logs/latest.log", mode="w")
latest_log.setFormatter(fmt)
logging.getLogger().addHandler(latest_log)

logger = logging.getLogger(__name__)

CMD_FORBID = ("(", ")", "[", "]", "{", "}", ";", ".", ",", ":")

CMDS = {
    "ping": (commands.ping, cmdhelp.ping),
    "say": (commands.say, cmdhelp.say),
    "stop": (commands.stop, cmdhelp.stop),
    "roll": (commands.roll, cmdhelp.roll),
    "dice": (commands.roll, cmdhelp.roll),
    "8ball": (commands.eightball, cmdhelp.eightball),
    "eightball": (commands.eightball, cmdhelp.eightball),
    "vote": (commands.vote, cmdhelp.vote),
    "poll": (commands.poll, cmdhelp.poll),
    "coinflip": (commands.coinflip, cmdhelp.coinflip),
    "coin": (commands.coinflip, cmdhelp.coinflip),
    "flip": (commands.coinflip, cmdhelp.coinflip),
    "wikipedia": (commands.wikipedia, cmdhelp.wikipedia),
    "wiki": (commands.wikipedia, cmdhelp.wikipedia),
    "w": (commands.wikipedia, cmdhelp.wikipedia),
    "xkcd": (commands.xkcd, cmdhelp.xkcd),
    "imgflip": (commands.imgflip, cmdhelp.imgflip),
    "meme": (commands.imgflip, cmdhelp.imgflip),
    "eval": (commands.evalexpr, cmdhelp.evalexpr),
    "math": (commands.evalexpr, cmdhelp.evalexpr),
    "=": (commands.evalexpr, cmdhelp.evalexpr),
}

class MyClient(discord.Client):
    def __init__(self, imgflip_login):
        self.imgflip_login = imgflip_login
        super().__init__()

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=";help"))
        logger.info("Ready")

    async def on_message(self, message):
        # don"t reply to bots
        if message.author.bot:
            return

        if message.content.startswith(";"):
            idx = message.content.find(" ")
            if idx < 0: idx = len(message.content)
            cmd = message.content[1:idx].strip()
            rest = message.content[idx:].strip()
            if any(a in cmd for a in CMD_FORBID):
                return
            try:
                if cmd in CMDS:
                    logger.info("running command: {}".format(message.content))
                    await CMDS[cmd][0](self, message, rest)
                elif cmd == "help" or cmd == "?":
                    logger.info("running help command: {}".format(message.content))
                    if len(rest) == 0:
                        await cmdhelp.help_general(self, message)
                    elif rest == "help" or rest == "?":
                        await cmdhelp.help_cmd(self, message, cmdhelp.help)
                    elif rest in CMDS:
                        await cmdhelp.help_cmd(self, message, CMDS[rest][1])
                    else:
                        await cmdhelp.unknown(self, message)
            except Exception as e:
                try:
                    await message.channel.send(":x: An unexpected error occured while performing this command.")
                except Exception as e2:
                    logger.warning("Could not reply with error message")
                logger.error("Unexpected error in command: {}".format(message.content))
                logger.exception(e)

    # Ensure polls and votes only have one response per person
    async def on_reaction_add(self, reaction, user):
        if user.bot: return
        message = reaction.message
        if message.author.id == self.user.id \
            and len(message.embeds) > 0 \
            and message.embeds[0].color == botutils.COLOR_POLL:

            users = reaction.users()
            u = await users.find(lambda u: u.id == user.id)
            if u is not None:
                for emoji in message.reactions:
                    if emoji != reaction:
                        await message.remove_reaction(emoji, u)


with open("token") as tokenfile:
    token = tokenfile.read()
    logger.info("Read token")

try:
    with open("imgflip") as imgflipfile:
        imgflip = imgflipfile.read().split("\n")
        logger.info("Read ImgFlip login")
except:
    logger.warning("Failed to read ImgFlip login")
    imgflip = None

client = MyClient(imgflip)
client.run(token)
