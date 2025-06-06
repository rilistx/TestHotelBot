from pydantic import Field

from pydantic_settings import BaseSettings


class MainEnvs(BaseSettings):
    bot_token: str = Field(..., alias="BOT_TOKEN")
    bot_admin: int = Field(..., alias="BOT_ADMIN")

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"
        extra = "allow"


envs = MainEnvs()
