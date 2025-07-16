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
GUILD_OBJ = discord.Object(id=GUILD_ID)
MOD_ROLE_ID = int(os.getenv('MOD_ROLE_ID'))

# Set up logging
print("Bot is starting...")

@bot.event
async def on_ready():
    
    print(f"logged in as {bot.user.name}")
    
    synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Synced {len(synced)} commands to the guild.")

@bot.tree.command(
    name="ping",
    description="Check the bot's latency",
    guild= GUILD_OBJ
)
async def ping(interaction: discord.Interaction):
    
    await interaction.response.send_message(
        f"Pong! Latency: {bot.latency * 1000:.2f} ms"
    )
    print(f"Ping command used by {interaction.user.name} in guild {interaction.guild.name}")
    
@bot.tree.command(
    name="kick",
    description="Kick a user from the server",
    guild= GUILD_OBJ
)
@app_commands.describe(
    user="The user to kick"
)
@commands.has_role(MOD_ROLE_ID)
async def kick(interaction: discord.Interaction, user: discord.User):
    if interaction.user.top_role <= user.top_role:
        await interaction.response.send_message("You cannot kick this user.", ephemeral=True)
        return
    
    try:
        await interaction.guild.kick(user)
        await interaction.response.send_message(f"User {user.name} has been kicked.")
        print(f"Kicked {user.name} from guild {interaction.guild.name}")
    except discord.Forbidden:
        await interaction.response.send_message("I do not have permission to kick this user.", ephemeral=True)
    except discord.HTTPException:
        await interaction.response.send_message("Failed to kick the user due to an HTTP error.", ephemeral=True)

@bot.tree.command(
    name="ban",
    description="Ban a user from the server",
    guild= GUILD_OBJ
)
@app_commands.describe(
    user="The user to ban"
)
@app_commands.has_role(MOD_ROLE_ID)
async def ban(interaction: discord.Interaction, user: discord.User):
    if interaction.user.top_role <= user.top_role:
        await interaction.response.send_message("You cannot ban this user.", ephemeral=True)
        return
    
    try:
        await interaction.guild.ban(user)
        await interaction.response.send_message(f"User {user.name} has been banned.")
        print(f"Banned {user.name} from guild {interaction.guild.name}")
    except discord.Forbidden:
        await interaction.response.send_message("I do not have permission to ban this user.", ephemeral=True)
    except discord.HTTPException:
        await interaction.response.send_message("Failed to ban the user due to an HTTP error.", ephemeral=True)
 
@bot.tree.error
async def on_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message("You do not have the required role to execute this command.", ephemeral=True)
        print(f"Error: {error} - User {interaction.user.name} in guild {interaction.guild.name}")









bot.run(TOKEN)

