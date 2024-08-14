from pydantic_settings import BaseSettings, SettingsConfigDict
import warnings
import importlib.metadata

try:
    current_version = importlib.metadata.version("wp-wr-batchupload-api")
except Exception:
    current_version = "0.0.0"
warnings.filterwarnings("ignore", category=DeprecationWarning)


# The class `Settings` defines various configuration settings for a project with default values and a configuration dictionary.
class Settings(BaseSettings):
    PROJECT_NAME: str = "DOCX TO PDF API"
    API_VERSION: str = current_version
    BASE_URL: str
    NAME: str
    EMAIL: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


settings = Settings()
