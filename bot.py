import discord
from discord.ext import commands
from discord import app_commands
import logging
import os
import dotenv

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Load environment variables
dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
MOD_ROLE_ID = int(os.getenv('MOD_ROLE_ID'))

# Set up logging
print("Bot is starting...")

@bot.event
async def on_ready():
    print(f"logged in as {bot.user.name}")
    
    synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Synced {len(synced)} commands to the guild.")

@bot.tree.command(name="ping", description="Check the bot's latency", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency: {bot.latency * 1000:.2f} ms")










bot.run(TOKEN)

