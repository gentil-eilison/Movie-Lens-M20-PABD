import requests
from django.conf import settings


class OmdbService:
    API_KEY = settings.OMDB_API_KEY
    BASE_URL = "https://www.omdbapi.com"

    def call(self, url: str, **kwargs):
        try:
            response = requests.get(
                url,
                params={
                    "apikey": self.API_KEY,
                    **kwargs,
                },
                timeout=10,
            )
        except TimeoutError:
            return {}

        data = response.json()
        if "Error" in data:
            return {}
        return data

    def get_movie(self, imdb_id: str):
        return self.call(f"{self.BASE_URL}/", i=f"tt{imdb_id}")
