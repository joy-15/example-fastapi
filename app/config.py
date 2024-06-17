import os
from pydantic_settings import BaseSettings,SettingsConfigDict

def get_env_file_path():
    base_dir = os.path.dirname(__file__) 
    venv_dir = os.path.dirname(base_dir)  
    env_file_path = os.path.join(venv_dir, ".env") 
    return env_file_path

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=get_env_file_path())

settings = Settings()