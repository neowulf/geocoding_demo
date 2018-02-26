import unittest

from geocoding import GeocodingContext, GeocodingStrategyHereApi, GeocodingStrategyGoogleApi


class GeocodingTest(unittest.TestCase):

    def fixture(self, context):
        result = context.first_address_match("41.8842", "-87.6388")
        if result['provider'] == 'google':
            self.assertTrue(result, ['425 W Randolph St, Chicago, IL 60606, USA'])
        elif result['provider'] == 'here':
            self.assertTrue(result, ['425 W Randolph St, Chicago, IL 60606, United States'])

    def test_here_api(self):
        here_api = GeocodingStrategyHereApi()
        context = GeocodingContext(here_api)
        self.fixture(context)

    def test_google_api(self):
        google_api = GeocodingStrategyGoogleApi()
        context = GeocodingContext(google_api)
        self.fixture(context)

    def test_bad_coords(self):
        pass

    def test_fallback(self):
        pass
