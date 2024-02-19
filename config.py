from pydantic import BaseSettings

class Settings(BaseSettings):
    RABBIT_USERNAME: str
    RABBIT_PASSWORD: str
    RABBIT_HOST: str
    RABBIT_VHOST: str
    DATABASE_MONGO_URL: str
    DATABASE_MYSQL_URL: str

    class Config:
        env_file = './.env'


settings = Settings()