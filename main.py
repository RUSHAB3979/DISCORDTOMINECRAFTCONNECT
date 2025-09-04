# Discord Minecraft Log Bot

import discord
from discord.ext import commands
import json
import os

import asyncio
import aiofiles
from discord.ext import tasks

# --- Configuration Loading ---
def load_config():
    """Loads the configuration from config.json."""
    if not os.path.exists('config.json'):
        print("Error: config.json not found. Please rename config.json.example to config.json and fill in your details.")
        exit()
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
DISCORD_BOT_TOKEN = config.get('discord_bot_token')
CHANNEL_ID = int(config.get('channel_id'))
MINECRAFT_LOG_PATH = config.get('minecraft_log_path')

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True  # Required for commands

bot = commands.Bot(command_prefix='!', intents=intents)

# --- Background Task for Log Monitoring ---
async def monitor_log_file(channel):
    """Monitors the Minecraft log file and sends new lines to the specified channel."""
    try:
        async with aiofiles.open(MINECRAFT_LOG_PATH, mode='r', encoding='utf-8', errors='ignore') as f:
            # Go to the end of the file before starting the loop
            await f.seek(0, 2)
            print(f"Tailing log file from the end: {MINECRAFT_LOG_PATH}")
            while True:
                line = await f.readline()
                if not line:
                    # No new line, wait a bit before checking again
                    await asyncio.sleep(1)
                    continue
                # Send the new log entry to the Discord channel, if it's not empty
                if line.strip():
                    await channel.send(f"```{line.strip()}```")
    except FileNotFoundError:
        print(f"Error: Log file not found at {MINECRAFT_LOG_PATH}. Log monitoring will not start.")
        if channel:
            await channel.send(f"Error: Minecraft log file not found at `{MINECRAFT_LOG_PATH}`. Please check your `config.json`.")
    except Exception as e:
        print(f"An error occurred in the log monitoring task: {e}")
        if channel:
            await channel.send(f"An unexpected error occurred while reading the log file. The monitoring task has stopped.")

@bot.event
async def on_ready():
    """Event that runs when the bot is connected and ready."""
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f'Found channel: #{channel.name}. Starting log monitoring...')
        # Start the long-running task in the background
        bot.loop.create_task(monitor_log_file(channel))
    else:
        print(f"Error: Could not find channel with ID {CHANNEL_ID}. Make sure the bot is in the server and the ID is correct. Log monitoring will not start.")

@bot.command()
async def ping(ctx):
    """A simple command to check if the bot is responsive."""
    await ctx.send('Pong!')

# --- Main Execution ---
if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN or DISCORD_BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN":
        print("Error: Discord bot token is not set in config.json.")
    else:
        try:
            bot.run(DISCORD_BOT_TOKEN)
        except discord.errors.LoginFailure:
            print("Error: Invalid Discord Bot Token. Please check your config.json.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
