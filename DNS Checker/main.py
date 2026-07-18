# Load libraries
import os
import json
from dotenv import load_dotenv
load_dotenv()

from Utilities import discord, config, cloudflare

# Load Current Ip
currentIp = config.GetCurrentIp()

if os.getenv("UPDATEDNS") == "True":
    zoneIds = json.loads(os.getenv("ZONEIDS", "[]"))
    records = json.loads(os.getenv("RECORDS", "[]"))

    for zoneId in zoneIds:
        print (f"Checking {zoneId} DNS records.")

        for record in records:
            print (f"Checking DNS for {record}.")

            dnsRecord = cloudflare.GetDNSRecord(zoneId, record)

            if not dnsRecord:
                print("Record Not Found.")
                continue

            name = dnsRecord["name"]
            previousIp = dnsRecord["content"]

            # Perform checks and notification steps
            if currentIp != previousIp:
                print(f"IP changed: {previousIp} → {currentIp}")

                discord.SendDiscordNotification(currentIp)
                cloudflare.UpdateDNSRecord(zoneId, dnsRecord["id"], name, currentIp)
                discord.SendDiscordUpdate(name)

            else:
                print("No IP change.")

else:
    previousIp = config.GetPreviousIp()

    # Perform checks and notification steps
    if currentIp != previousIp:
        print(f"IP changed: {previousIp} → {currentIp}")

        discord.SendDiscordNotification(currentIp)
        config.UpdateEnvIp(currentIp)

    else:
        print("No IP change.")