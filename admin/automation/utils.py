import re

from pandas import Series


def remove_urls(column: str):
    """Remove page URLs from column"""
    return re.sub(r" \(http[s]?://\S+|www\.\S+", "", column)


def cleanup_empty(series: Series):
    """Remove empty values in a column"""
    return series[series.notnull() & (series != "")]


def cleanup_urls(series: Series):
    """
    Clean up URLs from column
    - remove `www`
    - remove leading `/`
    """
    return series.str.replace(r"^https?://(www\.)?", "https://", regex=True).str.rstrip(
        "/"
    )
