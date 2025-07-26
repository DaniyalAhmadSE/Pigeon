from core.services.interfaces.i_heading_reader import IHeadingReader
from docx import Document


class HeadingReader(IHeadingReader):
    def __init__(self) -> None:
        super().__init__()

    def get_indexed_headings(self, source_path: str) -> dict[int, str]:
        document = Document(source_path)
        indexed_headings: dict[int, str] = {}

        for i, paragraph in enumerate(document.paragraphs):
            if (
                paragraph.style is None
                or paragraph.style.name is None
                or not paragraph.style.name.lower().startswith("heading")
            ):
                continue
            indexed_headings[i] = paragraph.text.split("\n")[0]

        return indexed_headings
