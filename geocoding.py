import abc
import configparser
import json
from urllib import request, parse


class GeocodingContext:
    """
    Define the interface of interest to clients.
    Maintain a reference to a Strategy object.
    """

    def __init__(self, strategy):
        self._strategy = strategy

    def first_address_match(self, lat, long):
        json_response = self._strategy.reverse_geocode(lat, long)
        result = self._strategy.extract_address(json_response)
        result = self._strategy.decorate_result(result)
        return result


class GeocodingStrategy():

    @abc.abstractmethod
    def reverse_geocode(self, lat, long):
        pass

    @abc.abstractmethod
    def extract_address(self, json_response):
        pass

    @abc.abstractmethod
    def decorate_result(self, result):
        pass

    def invoke_api(self, url, query_dict):
        queryparams = parse.urlencode(query_dict)

        with request.urlopen(url + '?' + queryparams) as response:
            html = response.read().decode('utf-8')
            json_response = json.loads(html)
        return json_response


class GeocodingStrategyHereApi(GeocodingStrategy):
    """
    API: https://developer.here.com/documentation/geocoder/topics/quick-start-geocode.html
    """

    def __init__(self, app_id=None, app_code=None):
        self.app_id = app_id
        self.app_code = app_code

        try:
            if self.app_id is None or self.app_code is None:
                config = configparser.ConfigParser()
                config.read('config.ini')
                here_config = config['Here']
                self.app_id = here_config['app_id']
                self.app_code = here_config['app_code']
        except:
            # TODO logging
            print('Please provide api secrets via config.ini or programmatically.')

    def decorate_result(self, result):
        return {
            'provider': 'here',
            'result': result
        }

    def reverse_geocode(self, lat, long):
        reverse_geocode_url = "https://reverse.geocoder.cit.api.here.com/6.2/reversegeocode.json"
        query_dict = {"app_id": self.app_id,
                      "app_code": self.app_code,
                      "mode": "retrieveAddresses",
                      "prox": "%s,%s" % (lat, long)}

        return self.invoke_api(reverse_geocode_url, query_dict)

    def extract_address(self, json_response):
        result = []
        for json_response_view in json_response['Response']['View']:
            for json_response_result in json_response_view['Result']:
                # The results are in ascending order closest to the provided geo co-ords
                if json_response_result['MatchLevel'] == 'houseNumber':
                    address = json_response_result['Location']['Address']['Label']
                    result.append(address)
                    # ignoring remaining results
                    break
        return result


class GeocodingStrategyGoogleApi(GeocodingStrategy):

    def __init__(self, app_key=None):
        self.app_key = app_key

        try:
            if self.app_key is None:
                config = configparser.ConfigParser()
                config.read('config.ini')
                here_config = config['Google']
                self.app_key = here_config['app_key']
        except:
            # TODO logging
            print('Please provide api secrets via config.ini or programmatically.')

    def decorate_result(self, result):
        return {
            'provider': 'google',
            'result': result
        }

    def reverse_geocode(self, lat, long):
        reverse_geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        query_dict = {
            'latlng': '%s,%s' % (lat, long),
            'key': self.app_key
        }

        return self.invoke_api(reverse_geocode_url, query_dict)

    def extract_address(self, json_response):
        result = []
        for json_response_result in json_response['results']:
            google_location_types = json_response_result['types']
            if 'street_address' in google_location_types:
                address = json_response_result['formatted_address']
                result.append(address)
                break
        return result
