# Load libraries
import os
import discord

# Runs when the comment is entered
def Handler(bot):
    async def on_message(message):
        if message.author == bot.user:
            return

        thread = message.channel
        print(f"On Message triggered in \"{thread.name}\" channel.")
        print("------")
        await bot.process_commands(message)

    return on_message