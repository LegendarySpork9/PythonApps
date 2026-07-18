# Runs when the bot starts
def Handler(bot):
    async def on_ready():
        print(f"Logged in as {bot.user}")

        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} commands.")

        except Exception as ex:
            print(f"Error syncing commands: {ex}")

        print("------")

    return on_ready