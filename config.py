import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

if not os.getenv("DEBUG") or os.getenv("DEBUG").lower() == "true":
    load_dotenv("./.env.test")
else:
    load_dotenv("./.env")


class Settings(BaseSettings):
    RABBIT_USERNAME: str
    RABBIT_PASSWORD: str
    RABBIT_HOST: str
    RABBIT_VHOST: str
    DATABASE_MONGO_URL: str
    DATABASE_MYSQL_URL: str


settings = Settings()
