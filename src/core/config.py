from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")

    database_hostname: str | None = None
    database_port: str | None = None
    database_password: str | None = None
    database_name: str = "Proj1"
    collection_name: str = "Proj1-Data"
    database_username: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_region_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("AWS_REGION_NAME", "AWS_REGION"),
    )
    aws_bucket_name: str | None = None
    database_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("DATABASE_URL", "MONGODB_URL"),
    )


settings = Settings()
