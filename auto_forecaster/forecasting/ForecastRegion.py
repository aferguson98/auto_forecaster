import datetime

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

        self.data = {}

    def add_spot_to_region(self, spot_point):
        """
        Adds a ForecastPoint to this ForecastRegion
        Parameters
        ----------
        spot_point: ForecastPoint
            the ForecastPoint to add to this region
        """
        self.spot_range.append(spot_point)

    def process_data(self, parameters_to_load=None):
        """

        Parameters
        ----------
        parameters_to_load

        Returns
        -------

        """
        data = TextForecast.get_files_from_region(self)

        if parameters_to_load is None:
            # find all parameters available
            parameters_to_load = NetCDF.get_all_params([next(iter(data))])

        for date_time in data.keys():
            # input setup
            time_to_use = date_time.replace(minute=0)
            max_time_to_use = date_time + datetime.timedelta(hours=36)
            input_data = NetCDF.open_from_forecast_point(
                self.spot_range, parameters_to_load,
                [time_to_use, max_time_to_use])

            # output setup
            output_data = TextForecast.open_file(data[date_time])

            # save into dict
            data[date_time] = {
                "input": input_data,
                "output": output_data
            }

        for dat in data:
            print(dat, data[dat])
