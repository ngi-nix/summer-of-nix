import argparse
import os
import re
import tempfile
import zipfile
from typing import Optional

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


def mktmpdir(zip_file_path):
    """Generates a temporary directory based on the ZIP file name"""
    base_name = os.path.splitext(os.path.basename(zip_file_path))[0]
    tmp_dir = os.path.join(tempfile.gettempdir(), f"{base_name}_unzipped")

    # Create the directory if it doesn't exist
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir


def unzip_notion_export(zip_file_path) -> Optional[str | None]:
    """Unzips exported Notion zip file to a temporary directory"""
    tmp_dir = mktmpdir(zip_file_path)
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)
        return tmp_dir
    except Exception:
        return None


def get_notion_projects(zip_file_path) -> Optional[str | None]:
    """Gets the CSV Projects file from a Notion zip"""
    unzipped_dir = unzip_notion_export(zip_file_path)

    if unzipped_dir is None:
        return None

    for file in os.listdir(unzipped_dir):
        if file.endswith("_all.csv") or not file.endswith(".csv"):
            continue

        return os.path.join(unzipped_dir, file)
    return None
