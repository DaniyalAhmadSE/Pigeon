from typing import Protocol


class IHeadingReader(Protocol):
    def get_indexed_headings(self, source_path: str) -> dict[int, str]: ...
