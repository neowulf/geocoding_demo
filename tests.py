import unittest

from geocoding import GeocodingContext, GeocodingStrategyHereApi, GeocodingStrategyGoogleApi


class GeocodingTest(unittest.TestCase):

    def fixture(self, context):
        result = context.first_address_match("41.8842", "-87.6388")
        # print(result)
        if result['provider'] == 'Google':
            self.assertTrue(result['result'], ['425 W Randolph St, Chicago, IL 60606, USA'])
        elif result['provider'] == 'Here':
            self.assertTrue(result['result'], ['425 W Randolph St, Chicago, IL 60606, United States'])
        else:
            raise Exception('Fix fixture!')

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

# import threading
# from http.server import HTTPServer
# import time
# from driver import GeocodeHttpRequestHandler
# from urllib import request, parse
# from urllib.request import Request, urlopen  # Python 3
#
# class GeocodingHttpServer(unittest.TestCase):
#
#     @unittest.skip("Causes 'http.client.BadStatusLine: Content-Type: application/json'")
#     def test_handler(self):
#         # # The GET request will be sent here
#         # # and any exceptions will be propagated through.
#         # server = HTTPServer(('0.0.0.0', 8888), GeocodeHttpRequestHandler)
#         # server_thread = threading.Thread(target=server.serve_forever)
#         # # Also tried this:
#         # # server_thread.setDaemon(True)
#         # server_thread.start()
#         # # Wait a bit for the server to come up
#         # time.sleep(1)
#         #
#         url = 'http://127.0.0.1:8000/reverse_geocode'
#         queryparams = parse.urlencode({
#             'latlng': '41.8842,-87.6388',
#             'provider': 'here'
#         })
#
#         r = Request(url + '?' + queryparams)
#         r.add_header('Content-Type', 'application/json')
#
#         with request.urlopen(r) as response:
#             html = response.read().decode('utf-8')
#             json_response = json.loads(html)
#         print(json_response)
