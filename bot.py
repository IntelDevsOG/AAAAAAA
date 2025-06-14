import discord
import yaml
import subprocess
import json
import os
from discord.ext import commands
from cogs.vps_commands import VPSCommands

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

TOKEN = config['discord_token']
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Load the VPSCommands cog
bot.add_cog(VPSCommands(bot))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

bot.run(TOKEN)

