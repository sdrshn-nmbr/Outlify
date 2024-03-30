from flask import Flask, request, redirect, url_for
#from postgrest_py import PostgrestClient
from dotenv import load_dotenv
import os
import requests
from pprint import pprint as pp

from supabase import create_client, Client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)


@app.route("/auth")
def test():
    choice = 0

    while choice != '-1':
        choice = input("Sign Up, Sign In, Sign Out, View Data (1, 2, 3, 4): ")

        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")
            res = supabase.auth.sign_up(
                {
                    'email': email,
                    'password': password
                }
            )
            #print(res)
        elif choice == '2':
            email = input("Email: ")
            password = input("Password: ")
            data, error = supabase.auth.sign_in_with_password({"email": email, "password": password})
            print(data)
            #if error:
            #    print(error)
            #    return {'error': error.message}, 400
        elif choice == '3':
            res = supabase.auth.sign_out()
        elif choice == '4':
            data = supabase.auth.get_user()
            print(data.user.id)


def forward_string():
    return "Hello"

# Connect to weather API
@app.route('/weather')
def get_weather():
    zipcode = input("Enter Zipcode: ")
    api_key = "882d7c4617b36d2101b88c388111c3a0"
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&appid={api_key}&units=imperial"
    print("Hello")
    response = requests.get(url)
    weather_data = response.json()

    if response.status_code == 200:
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        description = weather_data["weather"][0]["description"]

        print(f"Temperature: {temperature}°C\n Humidity: {humidity}%\n Description: {description}")
        prompt = f"What should I wear today? This is the weather in my city: Temperature: {temperature}°C\n Humidity: {humidity}%\n Description: {description}"
        messages = []
        messages.append({"roles": "user", "content": prompt})
        return generate_response(requests.Session(), messages)
    else:
        print("Error fetching weather data")
        #exit()


    # Call ollama
def generate_response(session, message):
    url_llama = "http://localhost:11434/api/chat"

    payload = {
        "model": "llama2-uncensored",
        'messages': message,
        "stream": False,
    }

    # Send POST request using the session
    response = session.post(url_llama, json=payload)

    # Check response
    if response.status_code == 200:
        result = response.json()["message"]["content"]

        pp(result)
    else:
        print("Request failed with status code:", response.status_code)
        print("Response:")
        print(response.text)  # Print error response

# Get preferences (outfit type)
def get_preferences():
    outfit_type = input("Enter 1 for Casual, 2 for Semi-formal, 3 for Formal")
    return outfit_type

# Get info for DB


if __name__ == "__main__":
    app.run(debug=True)