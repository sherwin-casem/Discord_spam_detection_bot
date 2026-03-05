import discord

async def punish_user(message: discord.Message):
    try:
        # Delete spam message
        await message.delete()

        # Timeout user (10 minutes)
        await message.author.timeout(
            duration=600,
            reason="Spam detected"
        )

    except Exception as e:
        print("Moderation error:", e)