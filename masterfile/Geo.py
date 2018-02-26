import urllib
from urllib.error import HTTPError
from django.conf import settings
import json


class findloc(object):

    def make_request(self, address):
        params = self.get_params(address)
        try:
             r = urllib.request.urlopen(self.API_URL + "?" + params)
        except HTTPError as e:
            return None
        return self.normalize_answer(json.loads(r.read()))

    def normalize_answer(self, ans):
        raise NotImplementedError

    def get_params(self, address):
        raise NotImplementedError

    @classmethod
    def query_address(cls, address, service):
        geocoders = [Googlefindloc(), Herefindloc()] if service == "google" else \
            [Herefindloc(), Googlefindloc()]

        for geo in geocoders:
            res = geo.make_request(address)
            if res:
                return res
        return {'status': 'failure', 'msg':'Enter valid input or Service response not valid'}

class Googlefindloc(findloc):

    API_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_params(self, address):
        return urllib.parse.urlencode({
            'address': address,
            'key': settings.GOOGLE_API_KEY
        })

    def normalize_answer(self, ans):
        result = ans['results'][0]
        return {
            'Location': result['formatted_address'],
            'latitude': result['geometry']['location']['lat'],
            'longitude': result['geometry']['location']['lng'],
        }


class Herefindloc(findloc):
    API_URL = "https://geocoder.cit.api.here.com/6.2/geocode.json"

    def get_params(self, address):
        return urllib.parse.urlencode({
            'searchtext': address,
            'app_id': settings.HERE_APP_ID,
            'app_code': settings.HERE_APP_CODE
        })

    def normalize_answer(self, ans):
        result = ans['view'][0]['result'][0]
        return {
            'Location': result['formatted_address'],
            'latitude': result['geometry']['location']['lat'],
            'longitude': result['geometry']['location']['lng'],
        }
