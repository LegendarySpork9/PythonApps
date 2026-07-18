# Load libraries
from dotenv import load_dotenv
load_dotenv()

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os

import discord
from discord.ext import commands

# Load classes
from Commands import checktags, raiseissue
from Events import onmessage, onready

# Load token
token = os.getenv("DISCORDTOKEN")

# Configure discord
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

# Configure bot
bot = commands.Bot(command_prefix="!", intents=intents)

bot.event(onready.Handler(bot))
bot.event(onmessage.Handler(bot))

bot.tree.command(name="checktags", description="Checks the tags on the post.")(checktags.Handler)
bot.tree.command(name="raiseissue", description="Raises an issue on GitHub.")(raiseissue.Handler)

if token is None:
    raise ValueError("DiscordToken environment variable not set.")

# Run bot
bot.run(token)
