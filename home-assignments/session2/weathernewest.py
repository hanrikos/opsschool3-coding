import sys
from weather import Weather, Unit


def main(city_name):
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location(city_name)
    forecasts = location.forecast[0]
    weather_condition = forecasts.text
    max_temperature = forecasts.high
    min_temperature = forecasts.low
    forecast_date = forecasts.date

    print(f"The weather in {city_name} today({forecast_date}) is {weather_condition} with temperatures trailing from {min_temperature}-{max_temperature} celsius.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Please enter city name: {sys.argv[0]} <city_name>")
    else:
        main(sys.argv[1])
