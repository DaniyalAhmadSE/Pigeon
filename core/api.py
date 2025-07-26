from core.configuration import Configuration
from core.interfaces.i_api import IApi
from core.services.export_manager import ExportManager
from core.services.heading_reader import HeadingReader
from core.services.interfaces.i_export_manager import IExportManager
from core.services.interfaces.i_heading_reader import IHeadingReader
from core.services.interfaces.i_preset_manager import IPresetManager
from core.services.json_i_o_manager import JsonIOManager
from core.services.preset_manager import PresetManager


class Api(IApi):
    def __init__(self) -> None:
        super().__init__()
        configuration = Configuration()

        self._heading_reader: IHeadingReader = HeadingReader()
        self._writer_service: IExportManager = ExportManager(
            self._heading_reader, configuration.temporary_data_directory_path
        )

        self._preset_manager: IPresetManager = PresetManager(
            configuration.presets_file_path, JsonIOManager()
        )

    def get_indexed_headings(self, source_path: str) -> dict[int, str]:
        return self._heading_reader.get_indexed_headings(source_path)

    def export(
        self,
        source_path: str,
        destination_path: str,
        excluded_heading_indices: list[int],
    ):
        return self._writer_service.export(
            source_path, destination_path, excluded_heading_indices
        )

    def save_preset(self, excluded_headings_indices: list[int], preset_name: str):
        self._preset_manager.save_preset(excluded_headings_indices, preset_name)

    def get_preset(self, preset_name: str) -> list[int]:
        return self._preset_manager.get_preset(preset_name)

    def get_all_presets(self) -> dict[str, list[int]]:
        return self._preset_manager.get_all_presets()
