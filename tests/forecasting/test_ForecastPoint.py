import unittest

from auto_forecaster.forecasting.ForecastPoint import ForecastPoint

expected_result = ["Test", 1]


class TestForecastPoint(unittest.TestCase):
    def test_add_new_forecast_point(self):
        forecast_point = ForecastPoint("Test", 1)
        result = [forecast_point.location_name, forecast_point.spot_id]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
