# Load libraries
import os
import requests

apiToken = os.getenv("APITOKEN")

headers = {
    "Authorization": f"Bearer {apiToken}",
    "Content-Type": "application/json"
}

# Gets the DNS record
def GetDNSRecord(zoneId, record):
    url = f"https://api.cloudflare.com/client/v4/zones/{zoneId}/dns_records"
    params = {"name": record, "type": "A"}

    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()

    result = r.json()["result"]

    if not result:
        return None

    return result[0]

# Updates the DNS record
def UpdateDNSRecord(zoneId, recordId, name, ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{zoneId}/dns_records/{recordId}"

    data = {
        "type": "A",
        "name": name,
        "content": ip,
        "ttl": 1,
        "proxied": False
    }

    r = requests.put(url, headers=headers, json=data)
    r.raise_for_status()