import discord
import datetime
import sys
import random

import botutils
import matheval

# * say
# * ping
#   count
#   counttop
# * roll
# * flip
# * eval
# * help
# * 8ball
# * wikipedia
# * xkcd
# * meme
# * vote
# * poll


async def ping(client, message, argstr):
    diff = round((datetime.datetime.utcnow() - message.created_at) / datetime.timedelta(milliseconds=1))
    await message.channel.send(f":ping_pong: Pong in {diff} ms!")


async def say(client, message, argstr):
    if len(argstr) > 0:
        await message.channel.send(argstr)


async def stop(client, message, argstr):
    if message.author.id == 297903701916385290:
        await client.close()


async def roll(client, message, argstr):
    dicestr = argstr.replace(" ","")
    try:
        rolls = botutils.roll_dice(dicestr)
        rolestr = ", ".join([str(r) for r in rolls])
        total = sum(rolls)
        msg = f":game_die: Rolls: `{rolestr}` (Sum: **{total}**)"
        if len(msg) > 2000:
            await message.channel.send(f":game_die: Too many roles to display. Sum: **{total}**")
        else: await message.channel.send(msg)
    except botutils.UserException as e:
        await message.channel.send(":x: Error rolling dice: " + str(e))


async def coinflip(client, message, argstr):
    if len(argstr) == 0:
        if random.randrange(2) == 0:
            msg = ":coin: Heads!"
        else:
            msg = ":coin: Tails!"
        await message.channel.send(msg)
    else:
        try:
            count = int(argstr)
        except:
            await message.channel.send(":x: That isn't a number")
            return
        if count > 2048:
            await message.channel.send(":x: Too many coins (maximum is 2048)")
            return
        heads = 0
        for i in range(count):
            if random.randrange(2) == 0:
                heads += 1
        await message.channel.send(f":coin: {heads} heads, {count - heads} tails")
        return


async def eightball(client, message, argstr):
    if len(argstr) == 0:
        await message.channel.send(":x: You must ask the Magic Eight Ball a question")
    else:
        response = random.choice(botutils.EIGHTBALL_ANSWERS)
        await message.channel.send(":8ball: " + response)

async def evalexpr(client, message, argstr):
    expr = "".join(argstr)
    if len(expr) > 2 and expr[0] == "`" and expr[-1] == "`":
        expr = expr[1:-1]
    try:
        res = str(matheval.eval_expr(expr))
        if len(res) > 2000:
            raise Exception("result is longer than 2000 characters")
        m = f":1234: {res}"
        if len(m) > 2000:
            m = res
        await message.channel.send(m)
    except Exception as e:
        await message.channel.send(f":x: Error: {str(e)}")

async def vote(client, message, argstr):
    if len(argstr) == 0:
        await message.channel.send(":x: You must specify a question to vote on")
        return
    embed = discord.Embed(title=argstr)
    embed.color = botutils.COLOR_POLL
    embed.set_author(name=message.author.name)
    msg = await message.channel.send(embed=embed)
    await msg.add_reaction("⬆️")
    await msg.add_reaction("⬇️")


async def poll(client, message, argstr):
    parts = argstr.split(";")
    if len(parts) == 0:
        await message.channel.send(":x: You must specify a poll question with at least one answer")
        return
    elif len(parts) == 1:
        await message.channel.send(":x: You must specify at least one answer (separate prompt and answers with semicolons)")
        return
    elif len(parts) > 10:
        await message.channel.send(":x: Too many answers, the maximum is 9")
        return
    elif len(parts[0]) == 0:
        await message.channel.send(":x: Poll question cannot be empty")
        return
    # create embed
    embed = discord.Embed(title=parts[0])
    embed.color = botutils.COLOR_POLL
    embed.set_author(name=message.author.name)
    body = "\n".join(["**" + botutils.NUM_EMOJIS[i+1] + "**: " + choice for i, choice in enumerate(parts[1:])])
    embed.description = body
    # send embed and reactions
    msg = await message.channel.send(embed=embed)
    for i in range(len(parts) - 1):
        await msg.add_reaction(botutils.NUM_EMOJIS[i+1])

async def wikipedia(client, message, argstr):
    await message.channel.send(botutils.wikipedia(argstr))

async def xkcd(client, message, argstr):
    try:
        result = botutils.xkcd(argstr)
        if result is None or "title" not in result:
            raise UserException("Failed to retrieve comic information")
    except botutils.UserException as e:
        await message.channel.send(":x: " + str(e))
        return

    title = str(result["num"]) + ": " + result["safe_title"]
    embed = discord.Embed(title=title)
    embed.color = botutils.COLOR_WEB
    embed.set_footer(text=result["alt"])
    embed.set_author(name="xkcd", url="https://xkcd.com")
    embed.set_image(url=result["img"])
    embed.url = "https://xkcd.com/{}".format(result["num"])
    await message.channel.send(embed=embed)

async def imgflip(client, message, argstr):
    if client.imgflip_login is None:
        await message.channel.send(":x: ImgFlip is not currently enabled.")
        return
    
    try:
        data = botutils.imgflip(argstr, client.imgflip_login)
    except botutils.UserException as e:
        await message.channel.send(":x: " + str(e))
        return

    embed = discord.Embed()
    embed.color = botutils.COLOR_WEB
    embed.set_image(url=data["url"])
    embed.url = data["page_url"]
    embed.description = data["page_url"];
    await message.channel.send(embed=embed)

