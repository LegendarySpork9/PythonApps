# Load libraries
import discord

# Load command
import Utilities.birthday as bd

# Makes or Updates the record of a user's birthday
async def Handler(interaction: discord.Interaction):
    thread = interaction.channel
    author = interaction.user
    print(f"ListBirthday triggered by \"{author}\" in {getattr(thread, 'name', 'Unknown')} channel.")

    await interaction.response.defer()

    birthdays = bd.LoadBirthdays()

    if not birthdays:
        await interaction.followup.send("No birthdays registered! Please run '/setbirthday' to set one")
        print("No birthdays registered")
        return

    lines = []
    
    for birthday in birthdays.values():
        lines.append(f"🎂 **{birthday['name']}** — {birthday['birthday']}")

    msg = "\n".join(lines)

    await interaction.followup.send(f"**Stored Birthdays:**\n{msg}")
    print(f"**Stored Birthdays:**\n{msg}")
    print("------")