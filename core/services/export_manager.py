from pathlib import Path
from docx import Document
from docx2pdf import convert
from core.services.interfaces.i_export_manager import IExportManager
from core.services.interfaces.i_heading_reader import IHeadingReader


class ExportManager(IExportManager):
    def __init__(
        self, reader_service: IHeadingReader, temporary_data_directory_path: str
    ) -> None:
        super().__init__()
        self._temporary_data_directory_path = temporary_data_directory_path
        self._reader_service = reader_service

    def export(
        self,
        source_path: str,
        destination_path: str,
        excluded_heading_indices: list[int],
    ):
        heading_indices = self._reader_service.get_indexed_headings(source_path).keys()

        doc = Document(source_path)

        start_removal = False
        for i, paragraph in enumerate(doc.paragraphs):
            if i in excluded_heading_indices:
                start_removal = True
            elif i in heading_indices:
                start_removal = False

            if start_removal is False:
                continue

            paragraph_element = paragraph._element  # type: ignore
            paragraph_element.getparent().remove(paragraph_element)  # type: ignore

        temporary_file_path = f"{self._temporary_data_directory_path}/{Path(destination_path).name.removesuffix("pdf")}docx"
        doc.save(temporary_file_path)

        Path(destination_path).parent.mkdir(parents=True, exist_ok=True)

        convert(temporary_file_path, destination_path)
        Path(temporary_file_path).unlink()
