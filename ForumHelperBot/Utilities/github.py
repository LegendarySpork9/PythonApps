# Load libraries
import os
import aiohttp

# Load model
import Models.githubvalues as gv

# Creates an issue in github from the forum post
async def RaiseGitIssue(title, body, tags):
    print("-> Raising issue...")

    githubToken = os.getenv("GITHUBTOKEN")
    application = ""
    repo = ""
    label = ""

    for tag in tags:
        tagName = tag.name
        print(f"-> Tag: {tagName}")

        if tagName in gv.repositories:
            print("-> Is Repo Tag: True")

            application = tagName
            print(f"-> Application: {application}")
            
            repo = gv.repositories[tagName]
            print(f"-> Repo: {repo}")

        if tagName in gv.tags:
            print("-> Is Label Tag: True")

            label = gv.tags[tagName]
            print(f"-> Label: {label}")

    if repo == "" or label == "":
        print("-> Repo or Label not found.")
        print("-> Issue not raised.")
        return False
    
    if repo == "LegendarySpork9/Other-Projects":
        title = f"{application} - {title}"

    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {githubToken}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"title": title, "body": body, "labels": [label]}

    print(f"-> URL: {url}")
    print(f"-> Headers: {headers}")
    print(f"-> Payload: {payload}")

    async with aiohttp.ClientSession() as session, session.post(url, headers=headers, json=payload) as resp:
        if resp.status == 201:
            issue = await resp.json()
            print(
                f"-> Issue created successfully: {issue.get('html_url', 'N/A')}"
            )
            print("-> Issue raised.")
            return True

        else:
            error = await resp.text()
            print(f"-> Failed to create issue: {error}")
            print("-> Issue not raised.")
            return False