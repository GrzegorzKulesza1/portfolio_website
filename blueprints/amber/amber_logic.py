import requests
import os

API_LOGIN = os.environ.get("API_LOGIN")
API_PASSWORD = os.environ.get("API_PASSWORD")
START_DATE = "today"
PARAMETERS = "t_2m:C,wind_dir_10m:d,wind_speed_10m:ms,wind_gusts_10m_1h:kmh,sunrise:sql,sunset:sql"
period = "PT23H:PT1H"
location = {
    "Jantar": [54.344455, 19.035535],
    "Wyspa Sobieszewska": [54.351128, 18.858831],
    "Hel": [54.615704, 18.828079],
    "Ustka": [54.589119, 16.856873],
    "Gdańsk": [54.413679, 18.625846],
}


class AmberBrain:
    """This class is responsible for catching weather attributes::

        data - collecting all data from API in json format

        avg_temperature - average temperature for the day

        avg_wind_speed - average wind speed for all day

        wind_strong_enough - returns True if the wind gusts are stronger than 40 km/h

        is_good_direction - return True if the wind blows from the north or northeast"""
    def __init__(self, city):
        self.city = city
        self.data = {}
        self.avg_temperature = 0
        self.avg_wind_speed = 0
        self.wind_strong_enough = False
        self.is_good_direction = False

    def get_data(self):
        """The function connects to the API."""
        lat, lon = location[self.city]
        api_endpoint = f"https://api.meteomatics.com/{START_DATE}Z{period}/{PARAMETERS}/{lat},{lon}/json"
        connection = requests.get(url=api_endpoint, auth=(API_LOGIN, API_PASSWORD))
        self.data = connection.json()

    def get_temperature(self):
        """The function extracts the temperature data and calculates the average temperature for the day. """
        all_temperatures = [single_hour['value'] for single_hour in self.data['data'][0]['coordinates'][0]['dates']]
        # Extracts only the full hour at which the sun rose or set. The full date format was YYYY-MM-DDThh:mm:ssZ
        sunrise = int((self.data['data'][4]['coordinates'][0]['dates'][0]["value"]).split("T")[1].split(":")[0])
        sunset = int((self.data['data'][5]['coordinates'][0]['dates'][0]["value"]).split("T")[1].split(":")[0])

        # Average daytime temperature.
        # I slice all_temperatures so that only those when the sun was shining remained in the list.
        self.avg_temperature = str(
            round(
                sum(all_temperatures[sunrise + 1:sunset]) / len(all_temperatures[sunrise + 1:sunset]), 2))\
            .replace(".", ",")

    def get_wind_speed(self):
        """The function extracts wind speed data and calculates the average wind speed for all day. """
        all_wind_speeds = [single_hour['value'] for single_hour in self.data['data'][2]['coordinates'][0]['dates']]
        self.avg_wind_speed = round(sum(all_wind_speeds) / len(all_wind_speeds) * 3.6)

    def check_wind(self):
        """The wind gusts and direction data. It also checks if the wind is strong enough
        and blows from the right direction."""
        all_wind_gusts = [single_hour['value'] for single_hour in self.data['data'][3]['coordinates'][0]['dates']]
        all_wind_directions = [single_hour['value'] for single_hour in self.data['data'][1]['coordinates'][0]['dates']]

        for wind_gust in all_wind_gusts:
            if wind_gust > 40:
                index = all_wind_gusts.index(wind_gust)
                self.wind_strong_enough = True
                if all_wind_directions[index] > 330 or all_wind_directions[index] < 60:
                    self.is_good_direction = True

    def get_all_attributes(self):
        """The function retrieves data and assigns the AmberProject class attributes about average temperature,
         average wind speed, gusts and direction."""
        self.get_data()
        self.get_temperature()
        self.get_wind_speed()
        self.check_wind()
