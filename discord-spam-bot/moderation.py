import discord
import datetime

async def punish_user(message: discord.Message):
    try:
        # Delete spam message
        await message.delete()

        # Timeout user for 10 minutes
        until = discord.utils.utcnow() + datetime.timedelta(minutes=10)

        await message.author.timeout(
            until,
            reason="Spam detected"
        )

        # Send warning message
        await message.channel.send(
            f"{message.author.mention} ⚠️ Stop spamming! You have been timed out for 10 minutes."
        )

    except Exception as e:
        print("Moderation error:", e)