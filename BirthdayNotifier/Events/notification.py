# Load libraries
import os
import asyncio

from discord.ext import commands, tasks

from datetime import datetime, timezone

# Load command
import Utilities.birthday as bd

bot = None

# Sets bot variable
def SetBot(discordBot):
    global bot
    bot = discordBot

# Wishes the user a happy birthday
@tasks.loop(hours = 24)
async def CheckBirthday():
    print("Birthday Check] Wishing happy birthdays...")

    channelId = os.getenv("NOTIFICATIONCHANNELID")
    now = datetime.now(timezone.utc)
    today = now.strftime("%m-%d")

    print(f"[Birthday Check] Checking birthdays for {today}")

    channel = await bot.fetch_channel(channelId)

    if channel is None:
        print(f"[Birthday Check] Channel Id {channelId} not found")
        return
    
    birthdays = bd.LoadBirthdays()
    matchesId = []
    matchesNames = []

    for userId, birthday in birthdays.items():
        try:
            date = datetime.strptime(birthday["birthday"], "%Y-%m-%d")
            
            if date.strftime("%m-%d") == today:
                matchesId.append(userId)
                matchesNames.append(birthday["name"])

        except Exception as ex:
            print(f"[Birthday Check] Error checking birthday for {birthday["name"]}: {ex}")

    for match in matchesId:
        await channel.send(f"🎉 Happy Birthday **<@{match}>**! 🎂")
        print(f"[Birthday Check] {matchesNames[matchesId.index(match)]} wished a happy birthday")

    print("Birthday Check] Happy birthdays wished")
    print("------")

@CheckBirthday.before_loop
async def BEforeCheckBirthdays():
    now = datetime.now(timezone.utc)
    target = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    if now >= target:
        target = target.replace(day = now.day + 1)
    
    delay = (target - now).total_seconds()
    print(f"Waiting {delay/3600:.2f} hours until next birthday check")
    print("------")
    await asyncio.sleep(delay)