import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize bot with a command prefix
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=':', intents=intents)

# Load extensions (cogs)

#bot.load_extension('cogs.leaderboard')

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')
    await bot.load_extension('cogs.session')
    print("session cog loaded")
    await bot.load_extension('cogs.users')
    print("user cog loaded")
    await bot.load_extension('cogs.leaderboard')
    print("leaderboard cog loaded")
    
bot.run(os.getenv("TOKEN"))