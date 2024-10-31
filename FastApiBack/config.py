from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NOTION_API_KEY: str
    NOTION_PROJECT_DATABASE_ID: str
    NOTION_PBI_DATABASE_ID: str 

    class Config:
        env_file = ".env"  # Points to the .env file

settings = Settings()
