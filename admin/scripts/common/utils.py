import argparse
import os
import re
import tempfile
import zipfile
from pathlib import Path

from pandas import Series


def remove_urls(column: str) -> str:
    """Remove page URLs from column"""
    return re.sub(r" \(http[s]?://\S+|www\.\S+", "", column)


def cleanup_empty(series: Series) -> Series:
    """Remove empty values in a column"""
    return series[series.notnull() & (series != "")]


def cleanup_urls(series: Series) -> Series:
    """
    Clean up URLs from column
    - remove `www`
    - remove leading `/`
    """
    return series.str.replace(r"^https?://(www\.)?", "https://", regex=True).str.rstrip(
        "/"
    )


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError(f"'{string}' is not a valid file directory.")


def zip_file_type(file_path):
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"{file_path} is not a valid file.")
    if not file_path.lower().endswith(".zip"):
        raise argparse.ArgumentTypeError(f"{file_path} is not a ZIP file.")
    return file_path


def load_credentials(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                content = file.read().strip()
                os.environ[filename] = content


def unzip_notion_export(zip_file_path: str) -> Path:
    """Unzips exported Notion zip file to a temporary directory"""
    tmp_dir = Path(tempfile.mkdtemp(prefix="son_notion_"))

    def extract_zip(target_zip: Path, destination: Path):
        with zipfile.ZipFile(target_zip, "r") as z:
            z.extractall(destination)

        for nested_zip in destination.rglob("*.zip"):
            nested_dest = nested_zip.parent / nested_zip.stem
            extract_zip(nested_zip, nested_dest)

    extract_zip(Path(zip_file_path), tmp_dir)
    return tmp_dir


def get_notion_projects(zip_file_path: str) -> tuple[Path, Path] | None:
    """Recursively finds subgrants file within an extracted Notion zip"""

    unzipped_dir = unzip_notion_export(zip_file_path)

    try:
        csv_path = next(unzipped_dir.rglob("*_all.csv"))
        return csv_path, unzipped_dir
    except StopIteration:
        print("No '_all.csv' file found in the export.")
        return None
