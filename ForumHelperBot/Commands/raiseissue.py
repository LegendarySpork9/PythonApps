# Load libraries
import os
import discord

# load command
from Utilities.github import RaiseGitIssue

# Runs when the command is entered
async def Handler(interaction: discord.Interaction):
    thread = interaction.channel
    print(f"RaiseIssue triggered by \"{getattr(thread, 'name', 'Unknown')}\" in {getattr(getattr(thread, 'parent', None), 'name', 'Unknown')} channel.")

    await interaction.response.defer()

    if interaction.guild is None:
        await interaction.followup.send("This command can only be used inside a server.")
        print("RaiseIssue triggered outside a server.")
        print("------")
        return

    if not isinstance(thread, discord.Thread) or not isinstance(thread.parent, discord.ForumChannel):
        await interaction.followup.send("This command must be run inside a forum post.", ephemeral=True)
        print("RaiseIssue triggered outside of a forum post.")
        print("------")
        return

    if isinstance(interaction.user, discord.Member):
        member = interaction.user
    else:
        member = await interaction.guild.fetch_member(interaction.user.id)

    adminRoleId = os.getenv("ADMINROLEID")
    print(member.roles)

    if adminRoleId is not None and not any(role.id == int(adminRoleId) for role in member.roles):
        await interaction.followup.send("You do not have permission to use this command.")
        print("RaiseIssue triggered by a user without admin role.")
        print("------")
        return

    title = thread.name
    tags = thread.applied_tags
    messages = [message async for message in thread.history(oldest_first=True)]
    body = messages[0].content
    attachments = messages[0].attachments

    print(f"Post Title: {title}")
    print(f"Post Tags: {tags}")
    print(f"Attachments: {len(attachments)}")

    if any(tag.name == "Question" for tag in tags):
        await interaction.followup.send("This command cannot be run on a question post.")
        print("RaiseIssue triggered on a question post.")
        print("------")
        return

    if "# New Feature Request:" in body or "# Bug Request:" in body:
        body = body.replace("# New Feature Request:\n", "")
        body = body.replace("# Bug Request:", "")
        body = body.replace("## ", "")

        print(f"Post Body: {body}")

        for attachment in attachments:
            if attachment.content_type and attachment.content_type.startswith("image"):
                body = f"{body}\n\n![{attachment.filename}]({attachment.url})"
                print(f"Image Attachment Added: {attachment.filename}")

            else:
                body = f"{body}\n\n[{attachment.filename}]({attachment.url})"
                print(f"File Attachment Added: {attachment.filename}")

        raised = await RaiseGitIssue(title, body, tags)

        if raised:
            await interaction.followup.send("Post raised as an issue on GitHub.")
            print("Issue raised successfully.")

            gitHubTag = os.getenv("GITHUBTAGID")

            if gitHubTag is not None and gitHubTag not in [tag.id for tag in tags]:
                await thread.add_tags(discord.Object(id=gitHubTag))
                print("GitHub tag added to post.")

        else:
            await interaction.followup.send("Failed to raise issue on GitHub.")
            print("Failed to raise issue.")

    else:
        await interaction.followup.send("The initial message is missing the new feature or bug form. Please amend message and run /raiseissue again.")
        print("Message missing new feature or bug form.")

    print("------")