import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from spam_detector import is_spam
from keyword_filter import is_suspicious
from moderation import punish_user

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.event
async def on_message(message: discord.Message):

    if message.author.bot:
        return

    # Step 1 — Fast keyword check
    if not is_suspicious(message.content):
        await bot.process_commands(message)
        return

    # Step 2 — AI verification
    spam = await is_spam(message.content)

    if spam:
        await punish_user(message)
        return

    await bot.process_commands(message)


bot.run(os.getenv("DISCORD_TOKEN"))