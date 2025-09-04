# Discord Minecraft Log Bot

This bot connects to a Minecraft server and sends log updates to a specified Discord channel in real-time.

## Features

-   Real-time monitoring of the Minecraft server's `latest.log` file.
-   Sends new log entries to a designated Discord channel.
-   Easy to configure with a `config.json` file.

## Prerequisites

-   Python 3.8 or higher
-   A Discord bot token
-   A Discord server where you have permission to add bots and manage channels
-   Access to the Minecraft server's log files

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/discord-minecraft-log-bot.git
    cd discord-minecraft-log-bot
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `config.json` file:**
    -   Rename `config.json.example` to `config.json`.
    -   Open `config.json` and fill in the required values:
        -   `discord_bot_token`: Your Discord bot token. You can get this from the [Discord Developer Portal](https://discord.com/developers/applications).
        -   `channel_id`: The ID of the Discord channel where you want the logs to be sent. To get the channel ID, enable Developer Mode in Discord (User Settings > Advanced > Developer Mode), then right-click the channel and select "Copy Channel ID".
        -   `minecraft_log_path`: The full path to your Minecraft server's `latest.log` file.

4.  **Run the bot:**
    ```bash
    python main.py
    ```

## How to Get a Discord Bot Token

1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2.  Click "New Application" and give it a name.
3.  Go to the "Bot" tab and click "Add Bot".
4.  Under the "Token" section, click "Copy" to get your bot token. **Do not share this token with anyone.**
5.  You will also need to enable the "Server Members Intent" and "Message Content Intent" under the "Privileged Gateway Intents" section.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
