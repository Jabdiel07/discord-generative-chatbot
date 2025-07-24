import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from translate import translate_text
from discord.commands import Option, SlashCommandGroup
from logging_config import setup_logging

# throughout the code, all of the @ are called decorators and it basically defines what a function will be doing. For the slash.command one, it allows Discord to recognize the upcoming function as a slash command

# loads the token from environment variable or config
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# here we initialize logging
logger = setup_logging(level=os.getenv("LOG_LEVEL", "INFO")) # if we want to change our level to debug, with this instruction, we can do that. The reason we use os.getenv is because this allows us to change the level in the terminal itself without having to hard code it. We can do this by typing 'export LOG_LEVEL=DEBUG' in the terminal before running the main file
                                                             # of course, we could also just do it the hard coded way, which would look something like 'logger = setup_logging(level=logging.INFO)'. The level will remain in DEBUG even when you stop running the file and run it again, as long as it's still the same terminal. If you happen to start a new terminal or restart it, then you'd have to export to DEBUG again
logger.info("Starting Translator Bot")

# set up intents (what kind of event the bot can listen to)
intents = discord.Intents.default()
intents.message_content = True # this is required to read message text from user

# Initialize the bot with command prefix (optional if using slash commands)
bot = commands.Bot(command_prefix ="!", intents=intents)

# here we're going to register the slash command
# name = "translate" is what the user needs to type after the slash in order to invoke the translation stuff. Since we're calling assigning it "translate", the user would need to do /translate
# the description part adds a description overview of what /translate does when the user is typing it out in the Discord chat
# in the function, Option is important because it lets Discord know what input it should ask us for
# the first parameter inside of the Option is the type we're expecting, the second one is a small text the user will see in Discord when choosing their target language choice, and the third one will show a list of choices for the user to choose from
# for the choices, if the user chooses one that's not defined in here, Discord won't let the user submit the reply. This is UI level, so if I tried running in the terminal, it'll probably run and throw me the exception error

@bot.slash_command(name="translate", description="Translate a phrase to English, Spanish, or French.")
async def translate(ctx, target_lang = Option(str, "Target language (english, spanish or french)", choices=["english", "spanish", "french"]), text = Option(str, "The text to translate")) -> str:
    logger.info(f"Translate command by {ctx.user} ->" f"{len(text)} chars to '{target_lang}'")

    try:
        result = translate_text(text, target_lang)
        await ctx.respond(f"{ctx.user.name} said: {result}") # this lets the bot reply back to the user in Discord
        #await ctx.respond(f"{ctx.user.name} translated {text} to {target_lang}: {result}")
        #print(ctx.user.name)
        # using dir in the following lines of code lets me see the attributes for the object I'm passing in
        # print(dir(ctx)) with this we can see the attributes to ctx, in it we can find user
        # print(dir(ctx.user)) with this we can see the attributes for user in ctx, in it we can find name and with this we can get the username for the user that initiated the translation query
        logger.info("Translation sent successfully")    
    except ValueError as e:
        logger.warning(f"ValueError in translate: {e}")
        await ctx.respond(str(e))
    except Exception:
        logger.exception("Unhandled exception during translation")

# basic event listener to confirm bot is online
@bot.event
async def on_ready():
    logger.info(f"{bot.user} has connected to Discord!")

# simple command telling the bot to do something, in this case, it'll say what's in the await statement.
@bot.command(name = "hello") # the user needs to type /hello to execute what's in the function below
async def hello(ctx):
    logger.info(f"Hello command invoked by {ctx.user.name}")
    await ctx.send("Hello! I'm alive.")

if not DISCORD_TOKEN:
    logger.error("DISCORD_TOKEN not set in environment")
    exit(1)
    
bot.run(DISCORD_TOKEN)