import requests
from requests.adapters import HTTPAdapter
from decouple import config

#
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


class MovieAPIService:
    BASE_URL = 'https://demo.credy.in/api/v1/maya/movies/'

    @staticmethod
    def get_movies(page=None):
        url = MovieAPIService.BASE_URL
        if page:
            url = f"{url}?page={page}"

        response = requests.get(
            url,
            auth=HTTPBasicAuth(settings.CLIENT_ID, settings.CLIENT_SECRET),
            timeout=5, verify=False
        )
        response.raise_for_status()
        return response.json()


get_movies = MovieAPIService.get_movies
