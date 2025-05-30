from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DRIVER = "postgresql+psycopg2"
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 5437
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'pomodoro'

    CACHE_HOST: str = "0.0.0.0"
    CACHE_PORT: int = 6379
    CACHE_NAME: int = 0

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"



