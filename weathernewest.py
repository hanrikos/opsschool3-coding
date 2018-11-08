import sys
import datetime
from weather import Weather, Unit

def main(city_name):
    weather = Weather(unit=Unit.CELSIUS)

    location = weather.lookup_by_location(city_name)
    forecasts = location.forecast
    today = datetime.datetime.today().strftime('%d %m %Y')

    for forecast in forecasts:
        city_weather_condition = forecast.text

        max_temperature = forecast.high
        min_temperature = forecast.low
        if forecast.date == today:
            break
    print("The weather in {} today is {} with temperatures trailing from {}-{} celsius".format(city_name, city_weather_condition, min_temperature, max_temperature ))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Please add city namet: {sys.argv[0]} <city_name>")
    else:
        main(sys.argv[1])
