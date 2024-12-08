from settings.config import Local, Production
from dotenv import load_dotenv
import os

load_dotenv()

config_space = os.getenv("CONFIG_SPACE", "LOCAL").upper()

config_mapping = {"LOCAL": Local, "PRODUCTION": Production}

auto_config = config_mapping.get(config_space)

if auto_config is None:
    raise EnvironmentError(f"CONFIG_SPACE is an unexpected value: {config_space}")
