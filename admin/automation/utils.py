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


def cleanup_series(series: Series):
    """Remove empty values, clean up URLs and remove duplicates"""
    series = cleanup_empty(series)
    series = cleanup_urls(series)
    return series.drop_duplicates()
