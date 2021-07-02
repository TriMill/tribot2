# TriBot 2
Rewrite of TriBot in Python (because why did I do it in rust???). The prefix is `;`

## Features
 - Create polls and votes
 - Evaluate mathematical expressions 
 - Roll dice, flip coins, and Magic 8-Ball
 - Search Wikipedia
 - View xkcd comics
 - (**TODO**) Competitive counting with a global leaderboard
 - Descriptive help for each command

## Permissions
TriBot requires the *Manage Messages* permission in order to remove double reactions from polls.

## Commands
Use `;help` to view a list of all commands, and `;help <cmd>` to view detailed help on a specific command.

### The `eval` command
The `eval` command uses syntax nearly identical to Python, but with a limited set of operators, keywords, and functions.

| Operator                    | Usage                                                                             |
|-----------------------------|-----------------------------------------------------------------------------------|
| `+` `-` `*` `/`             | Standard 4 functions                                                              |
| `+` `-`                     | Unary positive and negative signs                                                 |
| `**`                        | Exponentiation ("to the power of")                                                |
| `>` `<` `>=` `<=` `==` `!=` | Comparison operators                                                              |
| `//`                        | Fraction operator (different than Python, creates a fraction instead of dividing) |
| `and` `or` `not`            | Boolean operators                                                                 |

| Function                                                                                   | Usage                                                                               |
|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| `random`                                                                                   | Get a random number, from 0-1 by default or an integer up to the argument specified |
| `sqrt`                                                                                     | Square root                                                                         |
| `gcd`                                                                                      | Greatest common divisor                                                             |
| `abs`                                                                                      | Absolute value                                                                      |
| `floor` `ceil` `round`                                                                     | Floor, ceiling, and round functions                                                 |
| `exp` `log`                                                                                | The exp (e to the power of) and log (always base e) functions                       |
| `sin` `cos` `tan` `asin` `acos` `atan` `sinh` `cosh` `tanh` `asinh` `acos` `atanh` `atan2` | Trigonometric functions and their inverses, as well as atan2                        |
| `int` `float` `complex` `fraction` `str`                                                   | Conversion between different datatypes                                              |
| `numer` `denom`                                                                            | Numerator and denominator of a fraction                                             |

## Running
After `git clone`ing this repository, create a file named `token` containing your bot account's token. To start the bot, run `main.py`.

In order to make the `;imgflip` command functional, you must supply a username and password to an [ImgFlip](https://imgflip.com/) account. Create a file called `imgflip` and put the username on the first line and the password on the second. This information will be securely passed to the ImgFlip servers and will never be shown to the bot's users.

