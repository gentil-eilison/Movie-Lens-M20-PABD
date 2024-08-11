import requests
from django.conf import settings


class TmdbService:
    API_KEY = settings.TMDB_API_KEY
    BASE_URL = "https://api.themoviedb.org/3"

    def call(self, url: str, **kwargs):
        try:
            response = requests.get(
                url,
                params={
                    "api_key": self.API_KEY,
                    **kwargs,
                },
                timeout=10,
            )
        except TimeoutError:
            return {}

        data = response.json()

        if data.get("success"):
            return {}
        return data

    def get_movie(self, movie_id: str):
        return self.call(f"{self.BASE_URL}/movie/{movie_id}")
