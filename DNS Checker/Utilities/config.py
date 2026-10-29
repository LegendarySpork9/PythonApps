# Load libraries
import os
import requests

# Gets the current Ip
def GetCurrentIp():
    return requests.get("https://api.ipify.org").text.strip()

# Gets the previous Ip
def GetPreviousIp():
    return os.getenv("PREVIOUSIP")

# Updates the stored Ip value
def UpdateEnvIp(newIp):
    scriptLocation = os.getenv("FOLDERLOCATION")

    if not scriptLocation:
        print("[DNS Checker] FOLDERLOCATION environment variable is not set.")
        return

    with open(f"{scriptLocation}.env", "r") as f:
        lines = f.readlines()

    with open(f"{scriptLocation}.env", "w") as f:
        for line in lines:
            if line.startswith("PREVIOUSIP="):
                f.write(f"PREVIOUSIP={newIp}\n")

            else:
                f.write(line)