# Load libraries
import os
import discord

# Load command
from Utilities.tagchecker import TagCheck

# Runs when the comment is entered
def Handler(bot):
    async def on_message(message):
        if message.author == bot.user:
            return
        
        supportChannelId = os.getenv("SUPPORTCHANNELID")

        if message.channel.id != supportChannelId:
            return

        thread = message.channel
        print(f"On Message triggered by \"{thread.name}\" in {thread.parent.name} channel.")

        if isinstance(thread, discord.Thread) and isinstance(thread.parent, discord.ForumChannel):
            messages = [message async for message in thread.history()]
            print(f"Messages in thread: {len(messages)}")

            if len(messages) == 1:
                discordMessages, consoleMessages = TagCheck(thread.applied_tags)

                for msg in discordMessages:
                    index = discordMessages.index(msg)

                    try:
                        await thread.send(msg)
                        print(consoleMessages[index])

                    except Exception as ex:
                        print(f"Failed to send message: {ex}")

                if len(discordMessages) == 0:
                    await thread.send("Thank you for selecting the required tags.")
                    print("Required tags selected.")

        print("------")
        await bot.process_commands(message)

    return on_message