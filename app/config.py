from pydantic import BaseSettings

class Settings(BaseSettings):
    database_name: str
    database_host: str
    database_username: str
    database_password: str 
    secret_key: str
    Algorithm: str
    access_token_expire_min: int

    class Config:
        env_file = ".env"

settings = Settings()

