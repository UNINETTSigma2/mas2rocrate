import tomllib
from os import environ
from pathlib import Path

DEFAULT_XDG_CONFIG_HOME = Path.home() / '.config'
XDG_CONFIG_HOME = environ.get('XDG_CONFIG_HOME', DEFAULT_XDG_CONFIG_HOME)
VISIBLE_LOCATIONS = [XDG_CONFIG_HOME, Path('/usr/local/etc'), Path('/etc')]
INVISIBLE_LOCATIONS = [Path.cwd(), Path.home()]

CONFIG_FILE = 'mas2rocrate.toml'
CONFIG_PATHS = INVISIBLE_LOCATIONS + VISIBLE_LOCATIONS


class Config:
    ENDPOINT: str
    USERNAME: str
    TOKEN: str

    def is_valid(self):
        return self.ENDPOINT and self.USERNAME and self.TOKEN


def find_config_file():
    for path in CONFIG_PATHS:
        if path in INVISIBLE_LOCATIONS:
            filename = f'.{CONFIG_FILE}'
        else:
            filename = CONFIG_FILE
        attempt = path / filename
        if attempt.exists():
            return attempt
    raise FileNotFoundError


def read_config_file(filename: Path):
    with open(filename, "rb") as F:
        try:
            data = tomllib.load(F)
        except tomllib.TOMLDecodeError:
            raise ValueError(f"Syntax error in configfile {filename}: Are the values all quoted?")
    config = Config()
    config.ENDPOINT = data.get('endpoint')
    config.USERNAME = data.get('username')
    config.TOKEN = data.get('token')
    return config


def get_config():
    filename = find_config_file()
    return read_config_file(filename)
