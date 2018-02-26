import unittest

from geocoding import GeocodingContext, GeocodingStrategyHereApi


class GeocodingTest(unittest.TestCase):

    def test_here_api(self):
        here_api = GeocodingStrategyHereApi()
        context = GeocodingContext(here_api)
        result = context.first_address_match("41.8842", "-87.6388,250")
        self.assertEqual(result, ['425 W Randolph St, Chicago, IL 60606, United States'])
