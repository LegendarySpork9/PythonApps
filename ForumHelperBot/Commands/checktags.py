# Load libraries
import discord

# Load command
from Utilities.tagchecker import TagCheck

# Checks whether the required tags are present for a github issue
async def Handler(interaction: discord.Interaction):
    thread = interaction.channel
    bot = interaction.client
    print(f"CheckTags triggered by \"{getattr(thread, 'name', 'Unknown')}\" in {getattr(getattr(thread, 'parent', None), 'name', 'Unknown')} channel.")

    await interaction.response.defer()

    if not isinstance(thread, discord.Thread) or not isinstance(thread.parent, discord.ForumChannel):
        await interaction.followup.send("This command must be run inside a forum post.", ephemeral=True)
        print("CheckTags triggered outside of a forum post.")
        print("------")
        return

    messages = [message async for message in thread.history()]
    form = ""
    missing = ""

    print(f"Messages in post: {len(messages)}")

    for message in messages:
        if form == "" and ("# New Feature Request:" in message.content or "# Bug Request:" in message.content) and message.author == bot.user:
            form = message.content
            print("New feature request form found")

        if missing == "" and ("Post Type tag not found." in message.content or "Application tag not found." in message.content) and message.author == bot.user:
            missing = message.content
            print("Missing tag message found.")

        if form != "" and missing != "":
            break

    discordMessages, consoleMessages = TagCheck(thread.applied_tags)
    sentMessage = False

    for message in discordMessages:
        if message != form and message != missing:
            index = discordMessages.index(message)

            try:
                await interaction.followup.send(message)
                sentMessage = True
                print(consoleMessages[index])

            except Exception as ex:
                print(f"Failed to send message: {ex}")

    if len(discordMessages) == 0:
        await interaction.followup.send("Thank you for selecting the required tags.")
        sentMessage = True
        print("Required tags selected.")

    if not sentMessage:
        await interaction.followup.send("No tag changes were registered.")
        print("No registered tag changes.")

    print("------")