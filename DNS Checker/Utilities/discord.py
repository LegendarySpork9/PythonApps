# Load libraries
import os
import requests

# Sends a message to a discord channel
def SendDiscordNotification(ip):
    webhookURL = os.getenv("DISCORDWEBHOOKURL")
    userId = os.getenv("DISCORDUSERID")

    message = f"<@{userId}> :globe_with_meridians: Your external IP has changed to: `{ip}`"
    payload = {"content": message}

    requests.post(webhookURL, json=payload)

# Sends an update message to a discord channel
def SendDiscordUpdate(name):
    webhookURL = os.getenv("DISCORDWEBHOOKURL")
    userId = os.getenv("DISCORDUSERID")

    message = f"<@{userId}> :globe_with_meridians: Cloudflare DNS record for {name} has been updated."
    payload = {"content": message}

    requests.post(webhookURL, json=payload)