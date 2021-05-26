import json
import requests


class WeatherData:

    def __init__(self, lat, lon, above = 0) -> None:
        self.lat = lat
        self.lon = lon
        self.above = above
#https://api.met.no/weatherapi/locationforecast/2.0/complete.json?altitude=11&lat=68.58&lon=33.05
    def _get_data(self) -> json:
        url = 'https://api.met.no/weatherapi/locationforecast/2.0/complete.json'
        headers = {'user-agent': 'YrBot/1.0 github.com/LonelyDragon/yr-weater-bot'}
        r = requests.get(f'{url}?altitude={self.above}&lat={self.lat}&lon={self.lon}', headers=headers)
        return r.text
