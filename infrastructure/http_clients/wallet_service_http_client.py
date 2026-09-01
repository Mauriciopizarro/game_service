import requests
from config import settings
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class WalletServiceHttpClient:

    set_money_path = "/wallet/set_money"

    def set_money(self, user_id: str, amount):
        """Sets money in the user wallet via the money_service HTTP endpoint."""
        url = f"{settings.WALLET_API_URL}{self.set_money_path}"
        response = requests.post(url=url, json={
            "user_id": user_id,
            "amount": amount
        })
        response.raise_for_status()
        logger.info(f"Set money in money_service via HTTP for user {user_id}")