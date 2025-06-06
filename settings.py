from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 5437
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'pomodoro'

    CACHE_HOST: str = "0.0.0.0"
    CACHE_PORT: int = 6379
    CACHE_NAME: int = 0

    JWT_SECRET_KEY: str = 'secret_key'
    JWT_ALGORITHM: str = 'HS256'

    @property
    def db_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"



