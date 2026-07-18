# Load libraries
import os
import json

from datetime import datetime

# Loads the file location
file = os.getenv("BIRTHDAYFILE")

# Returns the converted date
def ParseBirthday(date):
    print("-> Parsing birthday...")

    formats = ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"]

    for fmt in formats:
        try:
            formattedDate = datetime.strptime(date, fmt).strftime("%Y-%m-%d")
            print(f"-> Formatted birthday: {formattedDate}")
            print("-> Parsed birthday")
            return formattedDate
        
        except ValueError:
            print("-> Failed to format birthday")
            continue

    return None

# Loads the birthdays
def LoadBirthdays():
    print("-> Loading birthdays...")

    if os.path.exists(file):
        with open(file, "r") as f:
            print("-> Birthdays loaded")
            return json.load(f)
    
    else:
        print("-> No file found")

    return {}

# Saves the birthday
def SaveBirthday(birthdayData):
    print("-> Saving birthday...")

    with open(file, "w") as f:
        json.dump(birthdayData, f, indent=4)

    print("-> Birthday saved")