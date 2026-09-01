import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

if not os.getenv("DEBUG") or os.getenv("DEBUG").lower() == "true":
    load_dotenv("./.env.test")
else:
    load_dotenv("./.env")


class Settings(BaseSettings):
    DATABASE_MONGO_URL: str
    DATABASE_MYSQL_URL: str
    WALLET_API_URL: str
    MULTIPLY_BET_AMOUNT: str


settings = Settings()
