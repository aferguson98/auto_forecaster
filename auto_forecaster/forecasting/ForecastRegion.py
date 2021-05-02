import datetime

import numpy as np
import tensorflow as tf
from tensorflow import keras

from auto_forecaster.io import TextForecast, NetCDF


class ForecastRegion:
    def __init__(self, name, region_id, spot_range):
        """

        Parameters
        ----------
        name: str
            the short-form name of this region
        region_id: int
            an arbitrary region ID for this region
        spot_range: list of ForecastPoint
            a list of all ForecastPoints for this regions
        """
        self.name = name
        self.region_id = region_id
        self.spot_range = spot_range

        # data management
        self.data = {}
        self.params = []
        self.tokeniser = None

        # file management
        self.total_files = 0
        self.files_loaded = 0
        self.adjust_total = 0
        self.adjust_loaded = 0
        self.loader = None

    def set_loader(self, loader):
        self.loader = loader

    def add_spot_to_region(self, spot_point):
        """
        Adds a ForecastPoint to this ForecastRegion
        Parameters
        ----------
        spot_point: ForecastPoint
            the ForecastPoint to add to this region
        """
        self.spot_range.append(spot_point)

    def calc_total_files(self, params_to_load, mode="train"):
        if mode == "test":
            data = TextForecast.get_files_from_region(self, "test")
        else:
            data = TextForecast.get_files_from_region(self, "train")
        if params_to_load is None:
            # find all parameters available
            parameters_to_load = NetCDF.get_all_params(list(data))
        self.total_files = len(data) * 36 * len(parameters_to_load)

    def process_data(self, mode="train", parameters_to_load=None):
        """

        Parameters
        ----------
        mode
        parameters_to_load

        Returns
        -------

        """
        if mode == "test":
            data = TextForecast.get_files_from_region(self, "test")
        else:
            data = TextForecast.get_files_from_region(self, "train")

        if parameters_to_load is None:
            # find all parameters available
            parameters_to_load = NetCDF.get_all_params(list(data))
        self.params = parameters_to_load
        """print("\n\nLOADING DATA FROM REGION: \033[42m\033[30m\033[52m",
              self.name, "\033[0m", end=" ")
        for spot in self.spot_range:
            print("\033[52m", spot.location_name, "\033[0m", end=" ")
        print("\n\nParams:", end=" ")
        for params in parameters_to_load:
            print("\033[34m\033[52m", params, "\033[0m", end=" ")"""

        training_for_tokeniser = []

        data_keys = list(data.keys())

        for key in range(len(data_keys)):
            date_time = data_keys[key]
            # input setup
            time_to_use = date_time.replace(minute=0)
            max_time_to_use = date_time + datetime.timedelta(hours=37)
            input_data = NetCDF.open_from_forecast_region(
                self, parameters_to_load, [time_to_use, max_time_to_use]
            )

            # output setup
            output_data = TextForecast.open_file(data[date_time])
            training_for_tokeniser.append(output_data)

            # save into dict
            self.data[date_time] = {
                "input": input_data,
                "output": output_data
            }

        if not self.tokeniser:
            # fit tokeniser on texts
            self.tokeniser = keras.preprocessing.text.Tokenizer(
                filters='!"#$%&()*+,-/:;<=>?@[\\]^_`{|}~\t\n',
                lower=False)
            self.tokeniser.fit_on_texts(training_for_tokeniser)
        for dates in self.data:
            self.data[dates]["output"] = np.asarray(
                self.tokeniser.texts_to_sequences(
                    [self.data[dates]["output"]]
                ), dtype=np.int
            )
