import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# loads the token from environment variable or config
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# set up intents (what kind of event the bot can listen to)
intents = discord.Intents.default()
intents.message_content = True # this is required to read message text from user

# Initialize the bot with command prefix (optional if using slash commands)
bot = bot = commands.Bot(command_prefix ="!", intents=intents)

# basic event listener to confirm bot is online
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

# simple command telling the bot to do something, in this case, it'll say what's in the print statement.
@bot.command(name = "hello") # the user needs to type /hello to execute what's in the function below
async def hello(ctx):
    await ctx.send("Hello! I'm alive.")

bot.run(DISCORD_TOKEN)