import requests as req
from dotenv import load_dotenv
import os


city = input('Enter the city name: ')

load_dotenv()

api_key = os.getenv('OPENWEATHER_API_KEY')

params = {
    "q": city,
    "appid": api_key,
    "units": "metric"
}

try:
    r=req.get(
    'https://api.openweathermap.org/data/2.5/weather',
    params=params,
    timeout=5
    )

    r.raise_for_status()


except req.exceptions.Timeout as errt:
    print(f"Timeout Error : {errt}")
    exit(1)

except req.exceptions.ConnectionError as errc:
    print(f"Connection Error: status code: {errc.response.status_code if errc.response else 'No response'}")
    exit(1)

except req.exceptions.HTTPError as errh:
    status_code = errh.response.status_code
    if status_code == 401:
        print("Error: Unauthorized. Check your API key.")
    elif status_code == 404:
        print("Error: City not found. Please check the city name.")
    elif status_code == 429:
        print("Error: Too many requests. You have exceeded the API rate limit.")
    elif 500 <= status_code < 600:
        print("Error: Internal server error. Please try again later.")
    else:
        print(f"HTTP Error: {errh}")
    exit(1)

except req.exceptions.RequestException as err:
    print(f"Error: something went wrong: {err}")
    exit(1)

data = r.json()
print(f"Temperature in {city}: {data['main']['temp']}°C")
print(f"Description: {data['weather'][0]['description']}")