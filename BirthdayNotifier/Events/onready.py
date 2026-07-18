# Load events
from Events import notification

# Runs when the bot starts
def Handler(bot):
    async def on_ready():
        print(f"Logged in as {bot.user}")

        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} commands.")

        except Exception as ex:
            print(f"Error syncing commands: {ex}")

        if not notification.CheckBirthday.is_running():
            notification.CheckBirthday.start()
            print("Started notification event")

        print("------")

    return on_ready