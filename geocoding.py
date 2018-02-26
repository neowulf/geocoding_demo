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
        return result


class GeocodingStrategy():

    @abc.abstractmethod
    def reverse_geocode(self, lat, long):
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
                address = json_response_result['Location']['Address']['Label']
                print(address)
                result.append(address)
                # ignoring remaining results
                break
        return result
