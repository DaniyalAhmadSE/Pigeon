import json
from typing import Any
from core.services.interfaces.i_json_i_o_manager import IJsonIOManager


class JsonIOManager(IJsonIOManager):
    def read(self, path: str) -> dict[Any, Any]:
        with open(path) as json_file:
            data = json.load(json_file)
        return data

    def write(self, content: dict[Any, Any], path: str):
        with open(path, "w") as json_file:
            json.dump(content, json_file)
