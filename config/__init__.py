import toml
from pathlib import Path

SETTINGS_PATH = Path(__file__).parent / "settings.toml"
SECRETS_PATH = Path(__file__).parent / "secrets.toml"

settings = toml.load(SETTINGS_PATH)
secrets = toml.load(SECRETS_PATH)

class AttrDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

settings = AttrDict(settings["project"])
secrets = AttrDict(secrets["auth"])

def update_token(token_name: str, new_token: str):
    secrets[token_name] = new_token
    with open(SECRETS_PATH, "w") as f:
        toml.dump({"auth": secrets}, f)