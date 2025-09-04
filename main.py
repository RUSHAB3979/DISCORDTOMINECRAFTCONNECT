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
    """Monitors the Minecraft log file, handling log rotation."""
    print("Starting log monitoring task...")
    current_inode = None
    position = 0

    while True:
        try:
            # Check if the file exists
            try:
                stat_result = os.stat(MINECRAFT_LOG_PATH)
                inode = stat_result.st_ino
            except FileNotFoundError:
                if current_inode is not None:
                    print(f"Log file '{MINECRAFT_LOG_PATH}' not found. It may have been removed.")
                    await channel.send(f"⚠️ Log file `{os.path.basename(MINECRAFT_LOG_PATH)}` disappeared. Will retry...")
                current_inode = None
                await asyncio.sleep(10)
                continue

            # Open the file and determine where to start reading
            async with aiofiles.open(MINECRAFT_LOG_PATH, mode='r', encoding='utf-8', errors='ignore') as f:
                # If inode is new, it's a new file.
                if inode != current_inode:
                    print(f"New log file detected (inode: {inode}).")
                    if current_inode is not None: # It's a rotation
                        await channel.send(f"ℹ️ New log file `{os.path.basename(MINECRAFT_LOG_PATH)}` detected (log rotation).")
                        position = 0 # Read new file from start
                    else: # It's the very first run
                        print("First run. Seeking to end of file to ignore old logs.")
                        position = await f.seek(0, 2) # Go to the end
                    current_inode = inode

                # Seek to our last known position
                await f.seek(position)

                while True: # Inner loop for reading
                    line = await f.readline()
                    if not line:
                        # End of file. Check for rotation before sleeping.
                        try:
                            if os.stat(MINECRAFT_LOG_PATH).st_ino != current_inode:
                                print("Inode changed mid-read. Breaking to re-open.")
                                break # Break inner loop to re-open file
                        except FileNotFoundError:
                            print("File removed mid-read. Breaking to re-check.")
                            break # Break inner loop

                        await asyncio.sleep(1)
                        continue

                    if line.strip():
                        await channel.send(f"```{line.strip()}```")
                    position = await f.tell() # Update position after reading

        except Exception as e:
            print(f"An unexpected error occurred in the log monitoring task: {e}. Restarting check in 30 seconds.")
            await channel.send(f"🔥 An unexpected error occurred. The bot will try to recover in 30 seconds.")
            current_inode = None # Reset state
            position = 0
            await asyncio.sleep(30)

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
