# Load libraries
import discord

# Load command
import Utilities.birthday as bd

# Makes or Updates the record of a user's birthday
async def Handler(interaction: discord.Interaction):
    thread = interaction.channel
    author = interaction.user
    print(f"Formats triggered by \"{author}\" in {getattr(thread, 'name', 'Unknown')} channel.")

    await interaction.response.defer()
    await interaction.followup.send("Accepted date formats are: `DD-MM-YYYY`, `YYYY-MM-DD`, `DD/MM/YYYY`")
    print("Accepted date formats are: `DD-MM-YYYY`, `YYYY-MM-DD`, `DD/MM/YYYY")
    print("------")