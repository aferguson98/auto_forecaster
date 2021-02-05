"""
TextForecast.py
-----------------
Deals with the I/O for NetCDF files
"""
import os


def open_file(file_location):
    if not os.path.exists(file_location):
        err_message = ("Couldn't open file {} as it could not be found. Check "
                       "the file exists and try again.")
        raise FileNotFoundError(err_message.format(file_location))
    with open(file_location) as forecast_file:
        text_forecast = forecast_file.read()

    if text_forecast:
        return text_forecast

    err_message = ("File {} is empty and as such cannot be used. Check the "
                   "file contains the expected forecast text and try again.")
    raise ValueError(err_message.format(file_location))
