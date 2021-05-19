# TriBot 2
Rewrite of TriBot in Python (because why did I do it in rust???). The prefix is `;`

## Features
 - Create polls and votes
 - (**TODO**) Evaluate mathematical expressions 
 - Roll dice, flip coins, and Magic 8-Ball
 - Search Wikipedia
 - View xkcd comics
 - (**TODO**) Competitive counting with a global leaderboard
 - Descriptive help for each command

## Permissions
TriBot requires the *Manage Messages* permission in order to remove double reactions from polls.

## Commands
Use `;help` to view a list of all commands, and `;help <cmd>` to view detailed help on a specific command.

## Running
After `git clone`ing this repository, create a file named `token` containing your bot account's token. To start the bot, run `main.py`.

In order to make the `;imgflip` command functional, you must supply a username and password to an [ImgFlip](https://imgflip.com/) account. Create a file called `imgflip` and put the username on the first line and the password on the second. This information will be securely passed to the ImgFlip servers and will never be shown to the bot's users.

