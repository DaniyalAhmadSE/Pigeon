from pathlib import Path
from platformdirs import user_data_dir


class Configuration:
    def __init__(self) -> None:
        self._app_name = "Pigeon"
        self._app_data_path: str = user_data_dir(self._app_name, ensure_exists=True)
        self._temporary_data_directory_path: str = f"{self._app_data_path}/tmp"
        self._presets_file_path: str = f"{self._app_data_path}/presets.json"

    @property
    def temporary_data_directory_path(self):
        self._ensure_temporary_directory_exists()
        return self._temporary_data_directory_path

    @property
    def presets_file_path(self):
        self._ensure_presets_file_exists()
        return self._presets_file_path

    def _ensure_presets_file_exists(self):
        path = Path(self._presets_file_path)
        if path.exists():
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._presets_file_path, "x") as f:
            f.write("{}")

    def _ensure_temporary_directory_exists(self):
        Path(self._temporary_data_directory_path).mkdir(parents=True, exist_ok=True)
