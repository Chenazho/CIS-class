#Jose Lazalde
#CIS245
#Week 7
#Project Draft


# python_test.py
import requests
import time
import json


print('Welcome to Weather Now! Access current weather data for over 200,000 cities.')
print('For a precise forecast, please enter the 5 digit U.S. Zip Code for you location')
print('or the name of the city, comma, and 2-letter country code, as highlighted below.')
print('Selections made without a country code may return inaccurate results / cities.')
print('Examples...Barcelona, GB / San Francisco, US / Mexico City, Mx...')


def main():


    api_key = "541fdf299b53aee1a64f6d7fa4d5d42e"  # Enter the API key you got from the OpenWeatherMap website
    base_url = "http://api.openweathermap.org/data/2.5/weather?"


# This is to complete the base_url, you can also do this manually to checkout other weather data available
    city_name = input("Enter city name or Zip Code: ")

# This is to complete the base_url, you can also do this manually to checkout other weather data available
    complete_url = base_url + "appid=" + '541fdf299b53aee1a64f6d7fa4d5d42e' + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]

        current_temperature = y["temp"]
        z = x["weather"]
        f_degreeCurrent = round((((current_temperature - 273.15) * 9) / 5) + 32)
        c_degreeCurrent = round(current_temperature - 273.15)

        weather_description = z[0]["description"]

        hmdt = x['main']['humidity']

        low_temp = x['main']['temp_min']
        max_temp = x['main']['temp_max']
        f_degreeLow = round((((low_temp - 273.15) * 9) / 5) + 32)
        f_degreeMax = round((((max_temp - 273.15) * 9) / 5) + 32)


        print(" Temperature (in fahrenheit) = " +
            str(f_degreeCurrent) +
            "\n Temperature in Centigrades = " +
                        str(c_degreeCurrent) +
            "\n description = " +
                str(weather_description) +
            "\n Current Humidity: ", hmdt, '%' +
            "\n Low Temperature (in F):  ", str(f_degreeLow) +
            "\n Max Temperature (in F):  ", str(f_degreeMax))

    else:
        print(" City Not Found ")


    option = input('Would you like to enter another City, Yes or No? ')
    # while loop for a yes selection or to exit the program (and to catch input errors)
    while not (option == 'yes' or option == 'no'):
        option = input('You did not enter a valid selection.\n'
                           'Please enter Yes to search another City or No to exit: ')
    if option == 'yes':
        print('')
        main()
    if option == 'no':
        print('Thank you for using our the application. Have a nice day!')





main()