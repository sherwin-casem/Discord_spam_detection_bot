# Discord Spam Bot

A Discord moderation bot that detects and punishes spam using a two-stage pipeline: a fast keyword filter followed by AI verification with OpenAI.

## Features

- **Keyword pre-filter** — Flags messages containing common spam phrases before calling the API, keeping costs and latency low.
- **AI verification** — Messages that pass the keyword check are classified by GPT-4o-mini as `SPAM` or `NOT_SPAM`.
- **Automatic moderation** — Confirmed spam is deleted, the author is timed out for 10 minutes, and a warning is posted in the channel.

## How it works

```
Message received
       │
       ▼
  Keyword match? ──no──► Process commands normally
       │
      yes
       ▼
  OpenAI spam check
       │
       ▼
  SPAM? ──no──► Process commands normally
       │
      yes
       ▼
  Delete message, timeout user, send warning
```

1. Every non-bot message is checked against a list of suspicious keywords (`keyword_filter.py`).
2. If no keywords match, the message is treated as clean and any bot commands are processed.
3. If a keyword matches, the full message is sent to OpenAI for a second opinion (`spam_detector.py`).
4. If the model returns `SPAM`, the bot deletes the message, applies a 10-minute timeout, and notifies the channel (`moderation.py`).

## Prerequisites

- Python 3.10+
- A [Discord bot application](https://discord.com/developers/applications) with:
  - **Message Content Intent** enabled
  - **Server Members Intent** enabled
  - Permissions to manage messages and moderate members (timeout)
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/discord-bot.git
   cd discord-bot/discord-spam-bot
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the `discord-spam-bot` directory:

   ```env
   DISCORD_TOKEN=your_discord_bot_token
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Invite the bot to your server**

   Use the OAuth2 URL generator in the Discord Developer Portal. Select the `bot` scope and enable at least:

   - Read Messages / View Channels
   - Send Messages
   - Manage Messages
   - Moderate Members

5. **Run the bot**

   ```bash
   python bot.py
   ```

   You should see `Bot is online as <bot-name>` in the terminal.

## Project structure

```
discord-bot/
├── discord-spam-bot/
│   ├── bot.py              # Entry point, message handler
│   ├── keyword_filter.py   # Fast keyword pre-filter
│   ├── spam_detector.py    # OpenAI spam classification
│   ├── moderation.py       # Delete, timeout, and warn
│   └── requirements.txt
└── README.md
```

## Customization

### Spam keywords

Edit the `SPAM_KEYWORDS` list in `keyword_filter.py` to add or remove trigger phrases:

```python
SPAM_KEYWORDS = [
    "free nitro",
    "discord.gg/",
    "crypto giveaway",
    # add your own...
]
```

### Timeout duration

Change the timeout length in `moderation.py`:

```python
until = discord.utils.utcnow() + datetime.timedelta(minutes=10)
```

### AI model

The spam detector uses `gpt-4o-mini` by default. You can switch models in `spam_detector.py` if needed.

## Notes

- Only messages that match a keyword are sent to OpenAI, which reduces API usage.
- The bot ignores messages from other bots.
- Moderation actions require sufficient role hierarchy — the bot's role must be above the target user's role.
- If a moderation action fails (missing permissions, etc.), the error is logged to the console and the bot continues running.

## License

No license file is included. Add one if you plan to distribute or open-source this project.
