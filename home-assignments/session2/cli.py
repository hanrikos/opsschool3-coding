import click
import sys
from weather import Weather, Unit
import datetime


def convert_to_int(s):
    try:
        ret = int(s)
    except ValueError:
        ret = float(s)
    return ret


def convert_date_format(date):
    converted_date = datetime.datetime.strptime(date, "%d %b %Y").strftime("%d/%m/%Y")
    return converted_date

def create_report(location, number_of_days, city, temperature_unit, multiple):

    forecasts = location.forecast[number_of_days]
    weather_condition = forecasts.text
    max_temperature = forecasts.high
    min_temperature = forecasts.low
    if multiple:
        forecast_date = convert_date_format(forecasts.date)
        print(f"{forecast_date} {weather_condition} with temperatures trailing "
              f"from {min_temperature}-{max_temperature} "
              f"{temperature_unit}")
    else:
        print(f"The weather in {city} today is {weather_condition} "
              f"with temperatures trailing from {min_temperature}-{max_temperature} "
              f"{temperature_unit}")


def check_number_eligibility(number_of_days, forecasts):
    if number_of_days > len(forecasts):
        sys.exit("Sorry man, the number you "
                 "added is way out of the limits of weather-api, "
                 "please request a forecast for less number of days")


def check_temperature_unit(unit):
    if unit == "-c":
        weather = Weather(unit=Unit.CELSIUS)
        temperature_unit = "celsius"
        return weather, temperature_unit
    elif unit == "-f":
        weather = Weather(unit=Unit.FAHRENHEIT)
        temperature_unit = "fahrenheit"
        return weather, temperature_unit


def current_weather(city, unit, forecast):
    weather, temperature_unit = check_temperature_unit(unit)
    location = weather.lookup_by_location(city)

    if forecast == "TODAY":
        n = 0
        create_report(location, n, city, temperature_unit, multiple=False)
    else:
        separated_number_from_string = forecast.split("+")[1]
        number_of_total_days = convert_to_int(separated_number_from_string)
        forecasts = location.forecast

        check_number_eligibility(number_of_total_days, forecasts)
        create_report(location, 0, city, temperature_unit, multiple=False)
        print("")
        print(f"Forecast for the next {number_of_total_days} days:")
        print("")
        for each_day_number in range(number_of_total_days):
            create_report(location, each_day_number, city, temperature_unit, multiple=True)


@click.command()
@click.option('--city')
@click.option('--unit', '-c', '-f')
@click.option('--forecast')
def main(city, unit, forecast):
    current_weather(city, unit, forecast)


if __name__ == "__main__":
    main()
