# Jose Lazalde
# Week 7: Project draft
# Date: 2/20/2022
# CIS 245
# Assignment: 7.2
# Your program must prompt the user for their city or zip code and request weather forecast data from openweathermap.org
# Your program must display the weather information in an READABLE format to the user

import json
import time
import requests


print('Welcome to Weather Now! Access current weather data for over 200,000 cities.')
print('For a precise forecast, please enter the 5 digit U.S. Zip Code for you location')
print('or the name of the city, comma, and 2-letter country code, as highlighted below.')
print('Selections made without a country code may return inaccurate results / cities.')
print('Examples...Barcelona, GB / San Francisco, US / Mexico City, Mx...')


def main():
##Main function for the program, allows user to input a zip code or city to receive current/future forecast
    url = 'https://api.openweathermap.org/data/2.5/weather'
    url_ext = 'https://api.openweathermap.org/data/2.5/forecast'
    location = input('Please enter the Zip Code or City, Country: ')
    while True:
        try:
            weather_current(location, url)
            weather_extended(location, url_ext)
            print('')
            more_weather()
            break
        except LookupError:
            print('')
            more_weather()
            break


def weather_current(location, url):
##Makes a GET request to the url for current weather, verifies connection is made, parses and displays the data"""
    if location.isdigit() is True:
        query_params = {'zip': location, 'APPID': 'e0658f792164bea0f30488a83ec7f9c9'}
    else:
        query_params = {'q': location, 'APPID': 'e0658f792164bea0f30488a83ec7f9c9'}
    response = requests.get(url, params=query_params, timeout=(5, 14))
    try_web(response, location)
    if response.status_code == 200:
        print('Connected....City Found')
    current_parsed = json.loads(response.text)
    current_formatted(current_parsed)


def weather_extended(location, url_ext):
##Makes a GET request to the url for extended forecast, parses and displays the data
    if location.isdigit() is True:
        query_params = {'zip': location, 'cnt': 16, 'APPID': 'e0658f792164bea0f30488a83ec7f9c9'}
    else:
        query_params = {'q': location, 'cnt': 16, 'APPID': 'e0658f792164bea0f30488a83ec7f9c9'}
    response = requests.get(url_ext, params=query_params, timeout=(5, 14))
    try_web(response, location)
    ext_parsed = json.loads(response.text)
    ext_formatted(ext_parsed)


def convert_temp(temp):
##Converts Kelvin temperatures to Fahrenheit and Celsius
    f_degree = round((((temp - 273.15)*9)/5)+32)
    c_degree = round(temp - 273.15)
    return f'{f_degree}{chr(176)}F / {c_degree}{chr(176)}C'


def try_web(response, location):
    """Try Except block to test the request was successful, additionally checking if the city or
    zip code entered is valid by using 404 status code"""
    try:
        response.raise_for_status()
    except requests.HTTPError as error0:
        if response.status_code == 404:
            if location.isdigit() is True:
                print(f"The zip code entered '{location}' was not found or is not valid.")
            else:
                if location.__contains__(','):
                    print(f"The city entered '{location[0:-2].title() + location[-2:].upper()}' was not found.")
                else:
                    print(f"The city entered '{location.title()}' was not found.")
        else:
            print('Even we do not have access to single digit zip codes.')
            print(f'{error0}')
    except requests.ConnectionError as error1:
        print('Error Connecting')
        print(error1)
    except requests.Timeout as error2:
        print('Timeout Error')
        print(error2)
    except requests.RequestException as error3:
        print('Something Else Went Wrong')
        print(error3)


def actual_formatted(parsed):
##Decodes the JSON data then formats the printable
##then formats the printable to output of the current weather
    city = str(json.dumps(parsed['name'])).replace('"', '')
    country = str(json.dumps(parsed['sys']['country'])).replace('"', '')
    timezone = int(json.dumps(parsed['timezone']))
    epoch_time = int(json.dumps(parsed['dt']))
    true_time = epoch_time + timezone
    current_time = time.strftime("%A, %b %d, %Y %I:%M %p (local time)", time.gmtime(true_time))
    temp = float(json.dumps(parsed['main']['temp']))
    conditions = str(json.dumps(parsed['weather'][0]['description'])).replace('"', '').title()
    print(f'Weather Report for {city}, {country} on {current_time}:\n'
          f'Current Temperature {convert_temp(temp)}\n'
          f'Current Conditions: {conditions}\n')


def ext_formatted(parsed):
##Decodes the JSON data
##then formats the printable output of the extended forecast
    print(f"{'36 Hour Forecast':30}{'Temperature':22}{'Conditions'}")
    # For loop to pull the data for every six (6) hours, approximate 36 hour forecast data return
    for i in range(1, 15, 2):
        epoch_time = int(json.dumps(parsed['list'][i]['dt']))
        timezone = int(json.dumps(parsed['city']['timezone']))
        true_time = epoch_time + timezone
        future_time = time.strftime("%a, %b %d %I:%M %p", time.gmtime(true_time))
        temp = float(json.dumps(parsed['list'][i]['main']['temp']))
        conditions = str(json.dumps(parsed['list'][i]['weather'][0]['description'])).replace('"', '').title()
        print(f'{future_time:30}{convert_temp(temp):22}{conditions}')


def extra_weather():
##Allows the user to look up another location or exit the program
    option = str(input('Would you like to enter another City, Yes or No? ')).lower().strip()
    # while loop for a yes selection or to exit the program (and to catch input errors)
    while not (option == 'yes' or option == 'no'):
        option = str(input('You did not enter a valid selection.\n'
                           'Please enter Yes to search another City or No to exit: ')).lower().strip()
    if option == 'yes':
        print('')
        main()
    if option == 'no':
        print('Thank you for using our the application. Have a nice day!')


main()