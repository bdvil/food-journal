import shutil

import yaml
from pydantic import BaseModel

from food_journal.constants import PROJECT_DIR


class Config(BaseModel):
    database_url: str

    service_url: str
    server_port: int


def load_config() -> Config:
    default_config_path = PROJECT_DIR / "example-config.yaml"
    config_path = PROJECT_DIR / "config.yaml"
    if not config_path.exists():
        shutil.copyfile(default_config_path, config_path)
    with open(config_path) as f:
        data = yaml.safe_load(f)
    return Config.model_validate(data)
