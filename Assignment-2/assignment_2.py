# import the necessary libraries
import pandas as pd
import requests
import json


# weatherstack_api
# please provide the necessary access key in the url
url = "http://api.weatherstack.com/current?access_key=5887a6e2b4fbd35b4fc98986893c2f9f&query={}"


# function to create the dataset,display 3 countries with the lowest temperature and City with the highest humidity
# provid the file_path of the csv as input
def getResult(file_path):

    df = pd.read_csv(file_path)
    duplicate_city_check = set()

    # adding the current_temp and current_humidity column to the df and initialise to 0
    df['current_temp'] = 0
    df['current_humidity'] = 0

    counter = 0

    # looping through every row of the df
    for i in range(len(df)):
        city = df['city'][i]

        # If condition to make sure same city is not processed again
        if city not in duplicate_city_check:
            duplicate_city_check.add(city)

            # passing the city to query param
            endpoint = url.format(city)
            response = requests.request("GET", endpoint)
            response = response.json()

            # checking if 'current' exists in response
            if 'current' in response:
                current_temp = int(response['current']['temperature'])
                current_humidity = int(response['current']['humidity'])
                df['current_temp'][i] = current_temp
                df['current_humidity'][i] = current_humidity
            else:
                continue

        # this break is to ensure the number requests to the weatherstack api is limited to 20
        # The free version of weather stack api supports only 250 requests/mo
        counter = counter+1
        if counter > 20:
            break

    # To convert the df to csv
    df.to_csv("./Results.csv")

    # choosing the top 10 rows as we restricted the loop to 20 requests
    df = df.head(10)

    # the df is sorted based on current_temp and ran through a loop to get 3 unique countries having lowest temperatures
    df = df.sort_values(by=['current_temp'])
    lowest_n_temp_countries = set()
    for j in range(len(df)):
        country = df['country'][j]
        if len(lowest_n_temp_countries) == 3:
            break
        lowest_n_temp_countries.add(country)

    print("3 countries with the lowest temperature", lowest_n_temp_countries)

    # .idmax() is used to get the index of the max humidity value
    max_humidity_index = df['current_humidity'].idxmax()
    max_humidity_city = df['city'][max_humidity_index]

    print("City with the highest humidity", max_humidity_city)


# main
getResult('F:\PYT assignment\Assignment-2\city_list.csv')
