"""
TextForecast.py
-----------------
Deals with the I/O for NetCDF files
"""
import glob
import os

from datetime import datetime


def open_file(file_location):
    if not os.path.exists(file_location):
        err_message = ("Couldn't open file {} as it could not be found. Check "
                       "the file exists and try again.")
        raise FileNotFoundError(err_message.format(file_location))
    with open(file_location) as forecast_file:
        forecast_lines = forecast_file.read().splitlines()

    if forecast_lines:
        text_forecast = ""
        for index, line in enumerate(forecast_lines):
            if ":" in line and "Outlook" not in line:
                text_forecast += forecast_lines[index + 1] + " "
        return text_forecast.strip()

    err_message = ("File {} is empty and as such cannot be used. Check the "
                   "file contains the expected forecast text and try again.")
    raise ValueError(err_message.format(file_location))


def open_files_from_glob_as_str(file_glob="*.txt"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "..", "data", "text")
    file_locations = os.path.join(data_dir, file_glob)
    result_str = ""
    for f in glob.glob(file_locations):
        result_str += " " + open_file(f)
    return result_str.strip()


def get_files_from_region(region, mode="train"):
    """
    Function to get all regional forecast file locations and their corresponding
    dates and times

    Parameters
    ----------
    mode
    region: ForecastRegion
        The region to find the text forecast file locations for

    Returns
    -------
    dict
        dictionary in format {datetime: file location, ...}
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if mode == "train":
        data_dir = os.path.join(base_dir, "..", "..", "data", "text")
    elif mode == "test":
        data_dir = os.path.join(base_dir, "..", "..", "data", "test")
    else:
        data_dir = ""
    file_locations = os.path.join(data_dir, "* " + region.name + ".txt")
    results = {}

    for f in glob.glob(file_locations):
        file_name = " ".join(os.path.basename(f).split(" ")[:2])
        date_time = datetime.strptime(file_name, '%Y-%m-%d %H%M')
        results[date_time] = f
    return results
