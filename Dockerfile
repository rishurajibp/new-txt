# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Create a logs directory
RUN mkdir -p /app/logs

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables (if needed)
ENV TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ENV WEBSITE_LOGIN_URL=https://example.com/login

# Run the Telegram bot
CMD ["python", "telegram_bot.py"]
