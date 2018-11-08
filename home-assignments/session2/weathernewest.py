import sys
from weather import Weather, Unit


def main(city_name):
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location(city_name)
    forecasts = location.forecast
    weather_condition = forecasts[0].text
    max_temperature = forecasts[0].high
    min_temperature = forecasts[0].low
    forecast_date = forecasts[0].date

    print("The weather in {} today({}) is {} with temperatures trailing from {}-{} celsius.".format(city_name, forecast_date, weather_condition, min_temperature, max_temperature))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Please enter city name: {sys.argv[0]} <city_name>")
    else:
        main(sys.argv[1])
