import yaml
from jinja2 import Environment


def parse(path: str):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        return yaml.safe_load(
            Environment().from_string(content).render(yaml.safe_load(content))
        )
