# Load model
import Models.standardvalues as sv

# Runs when the command is entered
def TagCheck(tags):
    print("-> Checking tags...")

    typeTagFound = False
    applicationTagFound = False
    discordMessages = []
    consoleMessages = []

    if len(tags) > 2:
        discordMessages.append(
            "Too many tags selected. Please select one type tag" \
            " and one application tag."
        )
        consoleMessages.append("Post has too many tags selected.")

        print("-> Tags checked.")
        return discordMessages, consoleMessages

    for tag in tags:
        tagName = tag.name
        print(f"-> Found Tag: {tagName}")

        if tagName in sv.tagBodies or tagName == "Question":
            typeTagFound = True
            print("-> Is Type Tag: True")

            if tagName in sv.tagBodies:
                discordMessages.append(sv.tagBodies[tagName])
                consoleMessages.append(f"Sent default body for tag: {tagName}")

                print("-> Messages added to arrays")

        if tagName in sv.applicationTags:
            applicationTagFound = True
            print("-> Is Application Tag: True")

    if not typeTagFound or not applicationTagFound:
        print(f"-> Type Tag Missing: {not typeTagFound}")
        print(f"-> Application Tag Missing: {not applicationTagFound}")

        message = ""

        if not typeTagFound:
            message = f"{message}{list(sv.missingTagBodies)[0]}\n\n"
            print("-> Added missing type tag message")

        if not applicationTagFound:
            message = f"{message}{list(sv.missingTagBodies)[1]}\n\n"
            print("-> Added missing application tag message")

        message = f"{message}{list(sv.missingTagBodies)[2]}"
        discordMessages.append(message)
        consoleMessages.append("Sent message body for missing tag(s)")

        print("-> Messages added to arrays")

    print("-> Tags checked.")
    return discordMessages, consoleMessages