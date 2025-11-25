
import yaml
from pathlib import Path


def load_config(file_path="config/settings.yaml"):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)
