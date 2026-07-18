# Load libraries
import discord

# Load command
import Utilities.birthday as bd

# Makes or Updates the record of a user's birthday
async def Handler(interaction: discord.Interaction, date: str):
    thread = interaction.channel
    author = interaction.user
    print(f"SetBirthday triggered by \"{author}\" in {getattr(thread, 'name', 'Unknown')} channel.")

    await interaction.response.defer()

    print(f"Inputted date: {date}")

    birthday = bd.ParseBirthday(date)

    if not birthday:
        await interaction.followup.send("Invalid date format! Please use one of the following: `DD-MM-YYYY`, `YYYY-MM-DD`, `DD/MM/YYYY`")
        print("Invalid date format used")
        return
    
    birthdayData = bd.LoadBirthdays()

    userId = str(author.id)
    birthdayData[userId] = {
        "name": str(author),
        "birthday": birthday
    }

    bd.SaveBirthday(birthdayData)

    await interaction.followup.send(f"Birthday set to '{birthday}' for {author}")
    print(f"{author}'s birthday set to {birthday}")
    print("------")