# Discord Minecraft Log Bot

This bot connects to a Minecraft server and sends log updates to a specified Discord channel in real-time. It is designed to be robust, with handling for log rotation to ensure it can run continuously.

## Features

-   Real-time monitoring of the Minecraft server's `latest.log` file.
-   **Log Rotation Handling:** Automatically detects when `latest.log` is archived and switches to the new file.
-   Sends new log entries to a designated Discord channel.
-   Easy to configure with a `config.json` file.
-   Includes a `!ping` command to check if the bot is responsive.

## Prerequisites

-   Python 3.8 or higher.
-   A Discord Server where you have Administrator permissions.
-   Access to the Minecraft server's log files.

---

## ⚙️ Setup and Configuration

Follow these steps carefully to get your bot up and running.

### Step 1: Create the Discord Bot

1.  **Go to the Discord Developer Portal:** Navigate to [https://discord.com/developers/applications](https://discord.com/developers/applications) and log in.
2.  **Create a New Application:** Click the "New Application" button. Give it a name (e.g., "Minecraft Log Bot") and click "Create".
3.  **Go to the "Bot" Tab:** In the left-hand menu, select the "Bot" tab.
4.  **Add a Bot:** Click the "Add Bot" button and confirm by clicking "Yes, do it!".
5.  **Get the Bot Token:** Under the bot's username, you'll see a "Token" section. Click "Reset Token" (or "Copy" if available) to reveal and copy your bot's token. **Treat this token like a password and never share it.** This is your `discord_bot_token`.
6.  **Enable Privileged Intents:** Scroll down to the "Privileged Gateway Intents" section. You **must** enable both:
    -   `SERVER MEMBERS INTENT`
    -   `MESSAGE CONTENT INTENT` (Required for the bot to see commands like `!ping`).

### Step 2: Invite the Bot to Your Server

1.  **Go to the "OAuth2" Tab:** In the left-hand menu, select the "OAuth2" tab, then click on "URL Generator".
2.  **Select Scopes:** In the "Scopes" section, check the `bot` scope.
3.  **Select Permissions:** A new "Bot Permissions" section will appear. At a minimum, your bot needs:
    -   `Read Messages/View Channels`
    -   `Send Messages`
4.  **Generate the Invite URL:** Copy the URL that is generated at the bottom of the page.
5.  **Invite the Bot:** Paste the URL into your browser, select the server you want to add the bot to, and click "Authorize".

### Step 3: Configure the Bot Script

1.  **Clone this Repository:**
    ```bash
    git clone https://github.com/your-username/discord-minecraft-log-bot.git
    cd discord-minecraft-log-bot
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create and Edit `config.json`:**
    -   Rename the `config.json.example` file to `config.json`.
    -   Open `config.json` with a text editor. It should look like this:
        ```json
        {
          "discord_bot_token": "YOUR_DISCORD_BOT_TOKEN",
          "channel_id": "YOUR_DISCORD_CHANNEL_ID",
          "minecraft_log_path": "/path/to/your/minecraft/server/logs/latest.log"
        }
        ```
    -   Fill in the values:
        -   `discord_bot_token`: The token you copied in Step 1.
        -   `channel_id`: The ID of the channel where logs should be sent. To get this, enable Developer Mode in Discord (`User Settings > Advanced > Developer Mode`), then right-click on your target channel and select "Copy Channel ID".
        -   `minecraft_log_path`: The **full, absolute path** to your Minecraft server's `latest.log` file.
          -   **Windows Example:** `C:\\Users\\YourUser\\Desktop\\MinecraftServer\\logs\\latest.log` (note the double backslashes `\\`).
          -   **Linux Example:** `/home/user/minecraft/logs/latest.log`.

### Step 4: Run the Bot

-   Open a terminal or command prompt in the bot's directory and run:
    ```bash
    python main.py
    ```
-   If everything is configured correctly, you will see messages in your console indicating the bot is logged in and monitoring the log file.

---

## Troubleshooting

-   **Error: `Invalid Discord Bot Token`**
    -   You may have copied the token incorrectly or reset it after copying. Go back to the Developer Portal and get the token again.
-   **Bot is offline in Discord.**
    -   Make sure the `python main.py` script is still running in your terminal. If it crashed, the console will show an error message.
-   **Bot is online, but no logs appear.**
    -   **Check the Path:** Double-check that `minecraft_log_path` in your `config.json` is the correct, full path to `latest.log`.
    -   **Check Permissions:** Make sure the user account running the Python script has permission to read the `latest.log` file.
    -   **Check Channel Permissions:** In Discord, ensure the bot has the `View Channel` and `Send Messages` permissions in the target channel.
-   **Error: `Could not find channel with ID...`**
    -   Make sure the `channel_id` is correct.
    -   Make sure the bot has been successfully invited to the Discord server that contains that channel.
