"""
NetCDF.py
---------
Deals with the I/O for NetCDF files
"""
import os

import iris


def open_file(file_location, constraints=None):
    if not os.path.exists(file_location):
        err_message = ("Couldn't open file {} as it could not be found. Check "
                       "the file exists and try again.")
        raise FileNotFoundError(err_message.format(file_location))
    return iris.load_cubes(file_location, constraints=constraints)


def save_file(file_location):
    pass
