# Telegram Bot

A Telegram bot that monitors messages for blocked words, sends Lakshya batch updates, and manages attendance polls.

## Features

- **Message Filtering**: Automatically deletes messages containing blocked words
- **Lakshya Updates**: Responds to "lakshya" mentions with batch information
- **Admin Commands**:
  - `/addword <word>`: Add a word to the blocked list (admin only)
  - `/removeword <word>`: Remove a word from the blocked list (admin only)
  - `/getid`: Get chat and thread IDs
  - `/sendpoll`: Manually send attendance poll
- **Scheduled Polls**: Sends daily attendance polls every Sunday at 10 AM

## Deployment

This bot is deployed on Railway.

### Environment Variables

Set the following environment variables in your Railway project:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `CHAT_ID`: The chat ID for the supergroup (default: -1002800090700)
- `ATTENDANCE_TOPIC_ID`: The topic ID for attendance polls (default: 290)

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables in a `.env` file or export them.

3. Run the bot:
   ```bash
   python bot.py
   ```

## Requirements

- Python 3.8+
- python-telegram-bot[job-queue]