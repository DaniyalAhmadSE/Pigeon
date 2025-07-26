from typing import Protocol


class IExportManager(Protocol):
    def export(
        self,
        source_path: str,
        destination_path: str,
        excluded_heading_indices: list[int],
    ): ...
