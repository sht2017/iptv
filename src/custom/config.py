from pathlib import Path

from config_parser import parse
from jsondb import JsonDB

CONFIG = parse("config.yaml")
context_data = JsonDB("db.json")
