from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    print(model_config)
    
    #MongoDB
    DATABASE_HOST: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = 'ETL'
    
settings = Settings()