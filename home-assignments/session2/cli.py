import click
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


def print_selected_location_weather_report(location, days_index, city, temperature_unit, multiple_weather_report=False):

    forecasts = location.forecast[days_index]
    weather_condition = forecasts.text
    max_temperature = forecasts.high
    min_temperature = forecasts.low
    if multiple_weather_report:
        forecast_date = convert_date_format(forecasts.date)
        print(f"{forecast_date} {weather_condition} with temperatures trailing "
              f"from {min_temperature}-{max_temperature} "
              f"{temperature_unit}")
    else:
        print(f"\n The weather in {city} today is {weather_condition} "
              f"with temperatures trailing from {min_temperature}-{max_temperature} "
              f"{temperature_unit}")


def check_number_eligibility(days_index, forecasts):
    if days_index > len(forecasts):
        max_number_of_days_user_can_enter = len(forecasts)
        raise Exception(f"The number you added is too big, the maximum number is {max_number_of_days_user_can_enter}")


def get_weather_information_for_chosen_unit(unit):
    if unit == "-c":
        weather = Weather(unit=Unit.CELSIUS)
        temperature_unit = "celsius"
        return weather, temperature_unit
    elif unit == "-f":
        weather = Weather(unit=Unit.FAHRENHEIT)
        temperature_unit = "fahrenheit"
        return weather, temperature_unit


def current_weather(city, forecast, units):

    weather, temperature_unit = get_weather_information_for_chosen_unit(units)
    location = weather.lookup_by_location(city)

    if forecast == "TODAY":
        print_selected_location_weather_report(location, 0, city, temperature_unit)
    else:
        separated_number_from_string = forecast.split("+")[1]
        number_of_total_days = convert_to_int(separated_number_from_string)
        forecasts = location.forecast

        check_number_eligibility(number_of_total_days, forecasts)
        print_selected_location_weather_report(location, 0, city, temperature_unit)
        print(f"\n Forecast for the next {number_of_total_days} days: \n")
        for each_day_number in range(number_of_total_days):
            print_selected_location_weather_report(location, each_day_number, city, temperature_unit, True)


@click.command()
@click.option('--city')
@click.option('--forecast')
@click.option('-f', 'units', flag_value='-f')
@click.option('-c', 'units', flag_value='-c')
def main(city, forecast, units):
    current_weather(city, forecast, units)


if __name__ == "__main__":
    main()
