from core.services.interfaces.i_json_i_o_manager import IJsonIOManager
from core.services.interfaces.i_preset_manager import IPresetManager


class PresetManager(IPresetManager):
    def __init__(
        self, presets_file_path: str, json_i_o_manager: IJsonIOManager
    ) -> None:
        self._json_i_o_manager = json_i_o_manager
        self._presets_file_path = presets_file_path

    def save_preset(self, excluded_headings_indices: list[int], preset_name: str):
        presets: dict[str, list[int]] = self._json_i_o_manager.read(
            self._presets_file_path
        )
        presets[preset_name] = excluded_headings_indices
        self._json_i_o_manager.write(presets, self._presets_file_path)

    def get_preset(self, preset_name: str) -> list[int]:
        try:
            return self._json_i_o_manager.read(self._presets_file_path)[preset_name]
        except:
            raise Exception("Preset not found")

    def get_all_presets(self) -> dict[str, list[int]]:
        return self._json_i_o_manager.read(self._presets_file_path)
