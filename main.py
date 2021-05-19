#!/usr/bin/python3
# https://discord.com/oauth2/authorize?client_id=??????&scope=bot&permissions=8192
import discord
import asyncio

import commands
import botutils
import cmdhelp

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
}

class MyClient(discord.Client):
    def __init__(self, imgflip_login):
        self.imgflip_login = imgflip_login
        super().__init__()

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=";help"))
        print("Ready")
        
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
            if cmd in CMDS:
                try:
                    await CMDS[cmd][0](self, message, rest)
                except Exception as e:
                    await message.channel.send(":x: An unexpected error occured while performing this command.")
                    raise e
            elif cmd == "help" or cmd == "?":
                if len(rest) == 0:
                    await cmdhelp.help_general(self, message)
                elif rest == "help" or rest == "?":
                    await cmdhelp.help_cmd(self, message, cmdhelp.help)
                elif rest in CMDS:
                    await cmdhelp.help_cmd(self, message, CMDS[rest][1])
                else:
                    await cmdhelp.unknown(self, message)

                    

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
    print("Read token")

try:
    with open("imgflip") as imgflipfile:
        imgflip = imgflipfile.read().split("\n")
        print("Read ImgFlip login")
except:
    print("Failed to read ImgFlip login")
    imgflip = None

client = MyClient(imgflip)
client.run(token)
