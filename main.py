import os
import requests
from datetime import datetime as dt

host_domain = "https://trackapi.nutritionix.com"

APP_ID = os.environ["APPLICATION_ID"]  # Your Application_ID of nutritionix.com trackapi site
APP_KEY = os.environ["APPLICATION_KEY"]  # Your Application_KEY of nutritionix.com trackapi site
SHEETY_USERNAME = os.environ["SHEETY_USERNAME"]  # Basic Authentication of Sheety project
SHEETY_PASSWORD = os.environ["SHEETY_PASSWORD"]  # Basic Authentication of sheety project

nl_exercise_endpoint = f"{host_domain}/v2/natural/exercise"

header = {
    'x-app-id': APP_ID,
    'x-app-key': APP_KEY,
}

parameters = {
    'query': input("What Exercise you did today: ")
}

response = requests.post(url=nl_exercise_endpoint, json=parameters, headers=header)
data = response.json()

exercise_name = data['exercises'][0]['name']
duration_mins = data['exercises'][0]['duration_min']
calories_burnt = data['exercises'][0]['nf_calories']

sheety_endpoint = os.environ["SHEETY_ENDPOINT"]
today = dt.now()

for exercise in data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%H:%M:%S"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    response_1 = requests.post(url=sheety_endpoint, json=sheet_inputs, auth=(SHEETY_USERNAME, SHEETY_PASSWORD))

    print(response_1.text)
