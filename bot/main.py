import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from translate import translate_text
from discord.commands import Option, SlashCommandGroup
from logging_config import setup_logging

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

logger = setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))
logger.info("Starting Translator Bot")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix ="!", intents=intents)

@bot.slash_command(name="translate", description="Translate a phrase to English, Spanish, or French.")
async def translate(ctx, target_lang = Option(str, "Target language (english, spanish or french)", choices=["english", "spanish", "french"]), text = Option(str, "The text to translate")) -> str:
    logger.info(f"Translate command by {ctx.user} ->" f"{len(text)} chars to '{target_lang}'")

    try:
        result = translate_text(text, target_lang)
        await ctx.respond(f"{ctx.user.name} said: {result}")
        logger.info("Translation sent successfully")    
    except ValueError as e:
        logger.warning(f"ValueError in translate: {e}")
        await ctx.respond(str(e))
    except Exception:
        logger.exception("Unhandled exception during translation")

@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord!")

@bot.command(name = "hello")
async def hello(ctx):
    logger.info(f"Hello command invoked by {ctx.user.name}")
    await ctx.send("Hello! I'm alive.")

if not DISCORD_TOKEN:
    logger.error("DISCORD_TOKEN not set in environment")
    exit(1)
    
bot.run(DISCORD_TOKEN)