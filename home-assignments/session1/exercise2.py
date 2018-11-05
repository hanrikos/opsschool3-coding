import requests
import json2html
from json2html import *
import csv


LOCATION_BY_IP_API = 'http://ip-api.com/json'
OUTPUT_DIRECTORY = "/home/hans/opsschool/opsschool3-coding/home-assignments/session1/"
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&APPID=9c8b160816fc48b0288a6136e0989b2a&units=metric'
CITY_LIST = "/home/hans/opsschool/opsschool3-coding/home-assignments/session1/city_list.csv"


def check_current_location(location_url):
    """
    :param location_url: Location detection api url
    :return: the location of the device that the script is running
    """
    response = requests.get(location_url)
    json_data = response.json()
    city = json_data["city"]
    country = json_data["country"]
    print(json_data)
    print(city + " , " + country)
    return city, country


def create_weather_report(api_url, country):
    """
    :param api_url: open weather map API url
    :param country: country that we received from location detection function
    :return: creates a txt file with the weather report of specific city
    also creates an html file with full weather info page
    """
    response = requests.get(api_url)
    json_data = response.json()
    print(json_data)

    # country_str = json_data["sys"]["country"]
    city_str = json_data["name"]
    description_str = json_data["weather"][0]["main"]
    temperature_str = json_data["main"]["temp"]

    #print to single txt file
    with open("{}special_weather_report_of_{}.txt".format(OUTPUT_DIRECTORY, city_str), "w") as text_file:
        print("The weather in {}, {} is {} and the temperature is {} °C".format(city_str, country, description_str, temperature_str), file=text_file)

    #print to full html file
    jsonPage = json2html.convert(json=json_data)
    html_file = open("{}full_special_weather_report_of_{}.html".format(OUTPUT_DIRECTORY, city_str), "w")
    html_file.write(jsonPage)
    html_file.close()


def create_multiple_weather_report(template_api_url, city_list):
    """
    :param template_api_url: the basis open weather map API url
    :param city_list: the list of the cities we want to know the weather
    :return: prints a list with weather info of the cities listed
    """
    with open(city_list, mode='r') as infile:
        reader = csv.reader(infile)
        with open('{}city_list_new.csv'.format(OUTPUT_DIRECTORY), mode='w') as outfile:
            # writer = csv.writer(outfile)
            mydict = {rows[0]: rows[1] for rows in reader}

        for key, value in mydict.items():
            new_api_url = template_api_url.replace("{city}", key).replace("{country}", value)
            response = requests.get(new_api_url)
            json_data = response.json()

            # country_str = json_data["sys"]["country"]
            city_str = json_data["name"]
            temperature_str = json_data["main"]["temp"]
            print("The weather in {}, {} is {} °C degrees".format(city_str, value, temperature_str))


def main():
    print("Checking location of the machine")
    city, country = check_current_location(LOCATION_BY_IP_API)
    new_weather_api_url = WEATHER_API_URL.replace("{city}", city).replace("{country}", country)
    print(new_weather_api_url)
    print("Creating weather report for ".format(city))
    create_weather_report(new_weather_api_url, country)
    print("Creatin weather report for listed cities")
    create_multiple_weather_report(WEATHER_API_URL, CITY_LIST)


if __name__ == "__main__":
    main()
