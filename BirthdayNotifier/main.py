# Load libraries
from dotenv import load_dotenv
load_dotenv()

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os

import discord
from discord.ext import commands

# Load classes
from Commands import setbirthday, listbirthday, formats
from Events import onmessage, onready, notification

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

# Configure notifications
notification.SetBot(bot)

bot.event(onready.Handler(bot))
bot.event(onmessage.Handler(bot))

bot.tree.command(name="setbirthday", description="Sets the user's birthday.")(setbirthday.Handler)
bot.tree.command(name="listbirthdays", description="Lists the registered birthdays.")(listbirthday.Handler)
bot.tree.command(name="formats", description="Lists the accepted date formats.")(formats.Handler)

# Run bot
bot.run(token)