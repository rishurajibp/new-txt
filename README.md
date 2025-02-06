# Web Scraping Project

This project extracts all video and PDF URLs from a website after login. The login credentials (ORG code, ID, and Password) are provided by the user through a Telegram bot.

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install the dependencies using `pip install -r requirements.txt`.
4. Update `config.py` with your Telegram bot token.
5. Run the Telegram bot using `python telegram_bot.py`.

## Usage

- Start the bot by sending `/start`.
- Follow the prompts to provide your ORG code, User ID, and Password.
- The bot will return the list of video and PDF URLs.
