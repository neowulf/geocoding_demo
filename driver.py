import json
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer

from geocoding import GeocodingContext, GeocodingStrategyHereApi, GeocodingStrategyGoogleApi


class GeocodeHttpRequestHandler(BaseHTTPRequestHandler):
    default_provider = 'google'

    geocode_proxy = {
        'google': GeocodingContext(GeocodingStrategyGoogleApi()),
        'here': GeocodingContext(GeocodingStrategyHereApi())
    }

    def reverse_geocode(self, query_params):
        try:
            lat, long = query_params['latlng'][0].split(',')
            request_provider = query_params['provider'][0].lower()
        except:
            self.send_error(400)
            raise

        try:
            result = self.geocode_proxy[request_provider].first_address_match(lat, long)
        except:
            try:
                result = self.geocode_proxy[self.default_provider].first_address_match(lat, long)
            except:
                self.send_error(500)
                raise

        return result

    def do_GET(self):

        dispatcher = {
            '/reverse_geocode': self.reverse_geocode
        }

        try:
            http_path, query_params = self.extract()
            route = dispatcher[http_path]
        except KeyError:
            # route not found
            self.send_error(404)
            raise

        result = route(query_params)

        # FIXME `curl` is printing the response headers as part of the response body
        # self.send_header('Content-Type', 'application/json')
        # self.end_headers()

        self.send_response(200)

        self.wfile.write(json.dumps(result).encode('utf-8'))

    def extract(self):
        print(self.path)
        path_query = self.path.split('?', 1)

        try:
            http_path = path_query[0]
        except:
            http_path = None

        try:
            query_params = urllib.parse.parse_qs(path_query[1])
        except:
            query_params = None

        return http_path, query_params


def run(server_class=HTTPServer, handler_class=GeocodeHttpRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
