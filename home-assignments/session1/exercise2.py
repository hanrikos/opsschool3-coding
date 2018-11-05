import json
import requests
import json2html
from json2html import *
import csv


LOCATION_BY_IP_API = 'http://ip-api.com/json'
OUTPUT_DIRECTORY = "/home/hans/opsschool/opsschool3-coding/home-assignments/session1/"
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&APPID=9c8b160816fc48b0288a6136e0989b2a&units=metric'
CITY_LIST = "/home/hans/opsschool/opsschool3-coding/home-assignments/session1/city_list.csv"


def check_current_location(location_url):
    response = requests.get(location_url)
    json_data = response.json()
    city = json_data["city"]
    country = json_data["country"]
    print(json_data)
    print(city + " , " + country)
    return city, country


def create_weather_report(api_url):
    response = requests.get(api_url)
    json_data = response.json()
    print(json_data)

    country_str = json_data["sys"]["country"]
    city_str = json_data["name"]
    description_str = json_data["weather"][0]["main"]
    temperature_str = json_data["main"]["temp"]

    #print to single txt file
    with open("{}special_weather_report_of_{}.txt".format(OUTPUT_DIRECTORY, city_str), "w") as text_file:
        print("The weather in {}, {} is {} and the temperature is {} °C".format(city_str, country_str, description_str, temperature_str), file=text_file)

    #print to full html file
    jsonPage = json2html.convert(json=json_data)
    html_file = open("{}full_special_weather_report_of_{}.html".format(OUTPUT_DIRECTORY, city_str), "w")
    html_file.write(jsonPage)
    html_file.close()


def create_multiple_weather_report(template_api_url, city_list):


    with open(CITY_LIST, mode='r') as infile:
        reader = csv.reader(infile)
        with open('{}city_list_new.csv'.format(OUTPUT_DIRECTORY), mode='w') as outfile:
            # writer = csv.writer(outfile)
            mydict = {rows[0]: rows[1] for rows in reader}

        for key, value in mydict.items():
            new_api_url = WEATHER_API_URL.replace("{city}", key).replace("{country}", value)
            response = requests.get(new_api_url)
            json_data = response.json()

            # country_str = json_data["sys"]["country"]
            city_str = json_data["name"]
            temperature_str = json_data["main"]["temp"]
            print("The weather in {}, {} is {} °C degrees".format(city_str, value, temperature_str))


def main():

    city, country = check_current_location(LOCATION_BY_IP_API)
    new_weather_api_url = WEATHER_API_URL.replace("{city}", city).replace("{country}", country)
    print(new_weather_api_url)
    create_weather_report(new_weather_api_url)
    create_multiple_weather_report(WEATHER_API_URL, CITY_LIST)

if __name__ == "__main__":
    main()