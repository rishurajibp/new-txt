# Use a more robust Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Create a logs directory
RUN mkdir -p /app/logs

# Copy the requirements file into the container
COPY requirements.txt .

# Install system dependencies and Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg2 \
    curl \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && CHROME_DRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}) \
    && wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && chmod +x /usr/bin/chromedriver \
    && rm /tmp/chromedriver.zip \
    && apt-get remove -y wget unzip gnupg2 curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables (if needed)
ENV TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ENV WEBSITE_LOGIN_URL=https://example.com/login

# Run the Telegram bot
CMD ["python", "telegram_bot.py"]
