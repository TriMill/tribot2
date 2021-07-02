import discord
from collections import namedtuple

import botutils

Help = namedtuple("Help", ["name", "short", "aliases", "usage", "desc", "examples"])

ping = Help(name="ping", short="Ping the bot", aliases=[], usage=["ping"], desc="Ping the bot to check that it is online, and shows the time it takes to respond in milliseconds.", examples=[";ping"])

say = Help(name="say", short="Make the bot say something", aliases=[], usage=["say <message>"], desc="Make the bot repeat whatever follows the command.", examples=["say I am sentient."])

coinflip = Help(name="coinflip", short="Flip one or more coins", aliases=["coin", "flip"], usage=["coinflip", "coinflip <n>"], desc="Flip one or more coins. `coinflip` without a parameter will flip a single coin, `coinflip <n>` will flip `n` coins and report how many landed heads and how many tails.", examples=["coinflip 30"])

stop = Help(name="stop", short="", aliases=[], usage=[], desc="yeah no", examples=[""])

roll = Help(name="roll", short="Roll dice", aliases=["dice"], usage=["roll <dice>"], desc="Roll dice specified using dice notation.", examples=["roll 1d20+3d4", "roll 2d12-1d6", "roll 5d7-12", "roll d6+d4"])

eightball = Help(name="8ball", short="Fortune telling", aliases=["eightball"], usage=["8ball <question>"], desc="Ask the Magic Eight-Ball any question. Answers are guarenteed to be 100% accurate.", examples=["8ball Will I get to keep the kids in the divorce?"])

vote = Help(name="vote", short="Allow people to vote with reactions", aliases=[], usage=["vote <question>"], desc="Allow everyone to vote on a question. Members can use the :arrow_up: and :arrow_down: reactions to vote on the question. Only one option can be chosen.", examples=["vote Should I get the kids in the divorce?"])

poll = Help(name="poll", short="Allow people to choose an option with reactions", aliases=[], usage=["poll <question>; <options...>"], desc="Allow members to choose their favorite option in a poll. Members can use the number reactions (:one:, :two:, :three:, etc.) to select their option. Options must be separated by semicolons.", examples=["poll Who should I get in the divorce?; Randolph; Kaiylaeigh; The dog"])

evalexpr = Help(name="eval", short="Evaluate a math expression", aliases=["math", "="], usage=["eval <expr>"], desc="Evaluate a math expression.", examples=["help poll", "help flip", "help", "help help"])

wikipedia = Help(name="wikipedia", short="Search Wikipedia", aliases=["wiki", "w"], usage=["wikipedia <query>"], desc="Search Wikipedia for the specified query. Responds with a Wikipedia search link with the `go` flag set, taking you directly to the first search result.", examples=["wikipedia Peter Kropotkin"])

xkcd = Help(name="xkcd", short="View an xkcd comic", aliases=[], usage=["xkcd", "xkcd <number>"], desc="View an xkcd comic by number or, if no number is specified, view the latest comic.", examples=["xkcd", "xkcd 1481"])

imgflip = Help(name="imgflip", short="Add text to a meme template with ImgFlip", aliases=["meme"], usage=["imgflip <template>;<text>", "imgflip <template>;<text1>;<text2>"], desc="Add text to a meme template using ImgFlip. Available templates are: " + ", ".join([f"`{x}`" for x in botutils.imgflip_templates.keys()]), examples=["imgflip drake; making memes yourself; using TriBot"])

help = Help(name="help", short="View help", aliases=["?"], usage=["help", "help <cmd>"], desc="View a list of commands with descriptions, or view information about a specific command.", examples=["help poll", "help flip", "help", "help help"])

categories = {"Random": [], "Web": [], "Polls": [], "Misc": []}
for x in [coinflip, roll, eightball]:
    categories["Random"].append("`{}`: {}".format(x.name, x.short))
for x in [xkcd, wikipedia, imgflip]:
    categories["Web"].append("`{}`: {}".format(x.name, x.short))
for x in [vote, poll]:
    categories["Polls"].append("`{}`: {}".format(x.name, x.short))
for x in [say, ping, evalexpr]:
    categories["Misc"].append("`{}`: {}".format(x.name, x.short))

async def help_general(client, message):
    embed = discord.Embed(title="TriBot Help")
    embed.color = botutils.COLOR_HELP
    embed.description = "Use `;help <cmd>` to view help on a specific command."
    for k, v in categories.items():
        s = "\n".join(v)
        embed.add_field(name=k, value=s, inline=False)
    await message.channel.send(embed=embed)


async def help_cmd(client, message, cmdinfo):
    embed = discord.Embed(title=f"Help for command `{cmdinfo.name}`:")
    embed.color = botutils.COLOR_HELP
    if len(cmdinfo.aliases) > 0:
        embed.add_field(name="Aliases", value=(", ".join([f"`{x}`" for x in cmdinfo.aliases])),inline=False)
    embed.add_field(name="Usage", value=(", ".join([f"`{x}`" for x in cmdinfo.usage])),inline=False)
    embed.add_field(name="Description", value=cmdinfo.desc,inline=False)
    embed.add_field(name="Examples", value=("\n".join([f"`{x}`" for x in cmdinfo.examples])),inline=False)
    
    await message.channel.send(embed=embed)


async def unknown(client, message):
    await message.channel.send(":x: Command not found. See `;help` for a list of commands.")
