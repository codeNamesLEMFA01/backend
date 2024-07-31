import os

from pydantic import BaseSettings, Field

class Settings(BaseSettings):
  DATABASE_URL: str = Field(..., env="DATABASE_URL")

settings = Settings()