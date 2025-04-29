"""
Telegram client module.
Provides interface for sending Telegram messages.
"""

import requests
from typing import Optional

class TelegramClient:
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram client.
        Args:
            bot_token (str): Telegram bot token
            chat_id (str): Target chat ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, message: str) -> Optional[dict]:
        """
        Send message to Telegram chat.
        Args:
            message (str): Message to send
        Returns:
            Optional[dict]: Response from Telegram API
        """
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message
        }
        response = requests.post(url, data=data)
        return response.json() if response.status_code == 200 else None 