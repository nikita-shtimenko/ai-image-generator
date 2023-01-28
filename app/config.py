import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

def config_init() -> None:
    if not os.path.isdir(Config.DIR_OUTPUT):
        os.mkdir(Config.DIR_OUTPUT)

    Config.DIR_OUTPUT_FILES_COUNT = len(os.listdir(Config.DIR_OUTPUT))

    load_dotenv()
    _config_init_env_variables()

    try:
        _config_validate_env_variables()
    except _InvalidApiKey as error_invalid_api_key:
        print(error_invalid_api_key)
        exit()
    
def _config_init_env_variables() -> None:
    Config.API_KEY_OPEN_AI = os.getenv("API_KEY_OPEN_AI", "")

def _config_validate_env_variables() -> None:
    if not Config.API_KEY_OPEN_AI:
        raise _InvalidApiKey()

@dataclass
class Config:
    API_KEY_OPEN_AI: str
    DIR_BASE = Path(__file__).resolve().parent.parent
    DIR_OUTPUT = os.path.join(DIR_BASE, "output")
    DIR_OUTPUT_FILES_COUNT: int = 0
    IMAGE_PROMPT_MIN_CHARACTERS_NUMBER: int = 5
    IMAGE_SIZES: tuple[str, str, str] = (
        "256x256",
        "512x512",
        "1024x1024"
    )

class _ConfigException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "ConfigException:"

class _InvalidApiKey(_ConfigException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{super().__str__()} InvalidApiKey: API key is invalid or not specified."