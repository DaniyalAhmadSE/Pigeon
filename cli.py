import argparse
import json
from typing import Optional
from core.interfaces.i_api import IApi


class Cli:
    def __init__(self, api: IApi) -> None:
        self._api = api
        self._source_path: str
        self._destination_path: str
        self._preset: Optional[str]
        self._args: argparse.Namespace

    def run(self):
        self._init_arguments()
        self._ensure_file_paths()

        if self._args.preset:
            excluded_headings_indices = self._api.get_preset(self._args.preset)
        else:
            excluded_headings_indices = self._get_exclusions()

        self._api.export(
            self._source_path, self._destination_path, excluded_headings_indices
        )

    def _get_exclusions(self):
        exclusion_source_choice = self._get_exclusion_source_choice()
        if exclusion_source_choice == "1":
            exclusions = self._get_exclusions_from_saved_presets()
        elif exclusion_source_choice == "2":
            exclusions = self._get_manual_exclusions()
            self._confirm_preset_saving(exclusions)
        else:
            raise Exception("Invalid source choice")
        return exclusions

    def _get_manual_exclusions(self):
        return [
            int(each.strip())
            for each in input(
                "Enter heading numbers to remove comma separated: "
            ).split(",")
        ]

    def _confirm_preset_saving(self, exclusions: list[int]):
        save_preset_choice = input("Do you want to save this preset? (y/n): ").lower()
        if save_preset_choice == "y":
            self._api.save_preset(
                exclusions,
                preset_name=input("Enter a name for this preset: "),
            )
        elif save_preset_choice != "n":
            raise Exception("Invalid choice")

    def _get_exclusions_from_saved_presets(self):
        print("Saved Presets:")
        all_presets = self._api.get_all_presets()
        print(json.dumps(all_presets, indent=4))
        return all_presets[input("Enter your preset of choice: ")]

    def _init_arguments(self):
        parser = argparse.ArgumentParser(description="")
        parser.add_argument("source", type=str, nargs="?", help="Source DOCX file path")
        parser.add_argument(
            "destination", type=str, nargs="?", help="Destination PDF file path"
        )
        parser.add_argument(
            "--preset", "-p", type=str, nargs="?", help="Exclusion preset to use"
        )
        self._args: argparse.Namespace = parser.parse_args()

    def _get_exclusion_source_choice(self):
        print("Headings:")
        print(json.dumps(self._api.get_indexed_headings(self._source_path), indent=4))
        print(
            "Enter 1 to use a saved preset.\n"
            "Enter 2 to manually specify exclusions.\n"
        )
        return input("Enter your choice: ")

    def _ensure_file_paths(self):
        source_path = self._args.source
        destination_path = self._args.destination

        if source_path is None:
            source_path = input("Enter source DOCX file path: ")
            if not source_path.endswith(".docx"):
                raise Exception("Invalid source file path")

        if destination_path is None:
            destination_path = input(
                "Enter destination PDF file path (default: source path with '.docx' replaced by '.pdf'): "
            )
            if not destination_path:
                destination_path = source_path[:-4]

        self._source_path = source_path
        self._destination_path = destination_path
