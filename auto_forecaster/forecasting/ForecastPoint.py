from auto_forecaster.io import NetCDF, TextForecast


class ForecastPoint:
    def __init__(self, location_name, spot_id):
        """
        A spot forecast region object

        Parameters
        ----------
        location_name: str
            an arbitrary location name used to identify this forecast region
        spot_id: int
            a list of spot IDs for this region
        """
        self.location_name = location_name
        self.spot_id = spot_id

        self.input_layer = []

    def load_point(self, parameters_to_load, date_range):
        """
        Parameters
        ----------
        date_range
        parameters_to_load: list of str
            List of NetCDF diagnostics to load from file
        """
        self.input_layer.append(
            NetCDF.open_from_forecast_region(
                self, parameters_to_load, date_range
            )
        )
