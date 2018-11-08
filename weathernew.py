import sys
from weather import Weather, Unit



def main(city_name):
    weather = Weather(unit=Unit.CELSIUS)
    city_weather_info = weather.lookup_by_location(city_name)
    print(city_weather_info.condition.text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Please add city namet: {sys.argv[0]} <city_name>")
    else:
        main(sys.argv[1])
