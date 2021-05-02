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
import numpy as np


selected_blend = "mix-spot_extract"


def open_file(file_location, constraints=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "..", "data")
    if not os.path.exists(file_location):
        err_message = ("Couldn't open file {} as it could not be found. Check "
                       "the file exists and try again.")
        raise FileNotFoundError(err_message.format(file_location))
    return iris.load_cubes(file_location, constraints=constraints)


def open_from_forecast_region(region, parameters_to_load, date_range):
    """

    Parameters
    ----------
    loader: FileLoader
    region: ForecastRegion
    parameters_to_load: list of str
    date_range: list of Datetime.date

    Returns
    -------
    list of numpy.array

    """
    loader = region.loader
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "..", "data")
    date_dir = date_range[0].strftime("%Y%m%dT%H00Z")
    input_data = [[] for i in parameters_to_load]
    min_date = date_range[0]
    max_date = date_range[1]
    difference = max_date - min_date
    days, seconds = difference.days, difference.seconds
    difference = int(days * 24 + seconds // 3600)
    date_range = [min_date + datetime.timedelta(hours=i)
                  for i in range(1, difference + 1)]

    for param in range(len(parameters_to_load)):
        parameter = parameters_to_load[param]
        param_data = []
        for date_time in date_range:
            date_file = date_time.strftime("%Y%m%dT%H00Z")
            file_location = os.path.join(data_dir, date_dir, selected_blend,
                                         date_file + "*" + parameter + ".nc")
            if not glob.glob(file_location):
                # expected less files due to accumulations not being hourly
                f = open('../../log.log', 'a')
                f.write("\n(!) WARNING | Couldn't find files " + file_location)
                f.close()
                region.total_files -= 1
                region.adjust_total -= 1
                param_data.append(np.asarray([-1.0, -1.0, -1.0, -1.0, -1.0,
                                              -1.0, -1.0, -1.0, -1.0, -1.0,
                                              -1.0, -1.0, -1.0, -1.0, -1.0]
                                             ).astype('float32'))
            for nc_file in glob.glob(file_location):
                cube = iris.load_cube(nc_file)
                points_data = []
                for spot in region.spot_range:
                    try:
                        points_data.append([cells[spot.spot_id]
                                            for cells in cube.data])
                    except IndexError as e:
                        # singular altitude coord so need to replicate
                        points_data.append([cube.data[spot.spot_id]] * 15)

                points_data_mean = []
                for i in range(len(points_data[0])):
                    points_data_mean.append(mean([h[i] for h in points_data]))
                param_data.append(
                    np.asarray(points_data_mean).astype('float32')
                )
                region.files_loaded += 1
                region.adjust_loaded += 1
            if region.adjust_total < -50 or region.adjust_loaded > 50:
                if loader:
                    loader.adjust(total=region.adjust_total,
                                  loaded=region.adjust_loaded)
                    region.adjust_total = 0
                    region.adjust_loaded = 0
        input_data[param] = np.asarray(param_data, dtype='float32')
    if loader:
        loader.adjust(total=region.adjust_total,
                      loaded=region.adjust_total)
    return np.array(input_data)


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
