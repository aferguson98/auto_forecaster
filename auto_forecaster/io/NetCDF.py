"""
NetCDF.py
---------
Deals with the I/O for NetCDF files
"""
import datetime
import glob
import os
from statistics import mean

import iris


selected_blend = "enukx-combine"


def open_file(file_location, constraints=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "..", "data")
    if not os.path.exists(file_location):
        err_message = ("Couldn't open file {} as it could not be found. Check "
                       "the file exists and try again.")
        raise FileNotFoundError(err_message.format(file_location))
    return iris.load_cubes(file_location, constraints=constraints)


def open_from_forecast_point(point, parameters_to_load, date_range):
    """

    Parameters
    ----------
    point: ForecastPoint
    parameters_to_load: list of str
    date_range: list of Datetime.date

    Returns
    -------
    list of numpy.array

    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "..", "data")
    input_data = []
    min_date = date_range[0]
    max_date = date_range[1]
    difference = int((max_date - min_date).seconds / 3600)
    date_range = [min_date + datetime.timedelta(hours=i)
                  for i in range(difference)]

    for parameter in parameters_to_load:
        param_data = []
        for date_time in date_range:
            date_dir = date_time.strftime("%Y%m%dT%H%MZ")
            file_location = os.path.join(data_dir, date_dir, selected_blend,
                                         "*" + parameter + ".nc")
            for nc_file in glob.glob(file_location):
                cube = iris.load_cube(nc_file)
                points_data = []
                for spot in point:
                    points_data.append([cells[spot.spot_id]
                                        for cells in cube.data])
                param_data.append([mean(cell) for cell in points_data])
        input_data.append(param_data)
    return input_data


def get_all_params(date_range):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "..", "data")

    date_to_use = date_range[0]
    date_dir = date_to_use.strftime("%Y%m%dT%H00Z")
    file_location = os.path.join(data_dir, date_dir, selected_blend,
                                 "*" + ".nc")

    params = []
    for f in glob.glob(file_location):
        f = os.path.basename(f)
        param = "-".join(f.split('-')[2:]).replace(".nc", "")
        if param not in params:
            params.append(param)
    return params
