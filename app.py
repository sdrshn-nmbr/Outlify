from flask import Flask, request, redirect, url_for, render_template, flash

# from postgrest_py import PostgrestClient
from dotenv import load_dotenv
import os
import requests
from pprint import pprint as pp
import re

from supabase import create_client, Client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)
app.config['SECRET_KEY'] = "naskDASKJDnasSDAksjn209u543"

@app.route("/")
def home():
    user = supabase.auth.get_user()

    if user:
        print(user)
        return render_template('main.html')
    else:
        return render_template('login.html')


@app.route("/signup")
def signup_page():
    return render_template('signup.html')


@app.route("/preferences")
def preferences_page():
    user = supabase.auth.get_user()
    print(user.user)
    return render_template('preferences.html')


@app.route('/login_func', methods=["post"])
def login_func():
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        data, error = supabase.auth.sign_in_with_password({"email": email, "password": password})
    except:
        flash('Incorrect login')
        return redirect('/')

    return redirect('/')


@app.route('/signup_func', methods=['post'])
def signup_func():
    email = request.form.get("email")
    password = request.form.get("password")
    location = request.form.get("location")
    
    pattern = '^[0-9]{5}(-[0-9]{4})?$'
    if not re.match(pattern, location):
        flash('Invalid zip code')
        return redirect('/signup')

    try:
        res = supabase.auth.sign_up(
            {
                'email': email,
                'password': password
            }
        )
        
        print(res)
    except:
        flash('Email may already be in use')
        flash('Password must be more than 6 characters long')
        return redirect('/signup')

    return redirect('/')


@app.route('/signout')
def signout_func():
    res = supabase.auth.sign_out()
    return redirect('/')


@app.route("/auth")
def test():
    choice = 0

    while choice != '-1':
        choice = input("Sign Up, Sign In, Sign Out, View Data (1, 2, 3, 4): ")


def llava_scan(path):
    url_llama = "http://localhost:11434/api/chat"
    prompt = (
        f"{path} classify this as a clothing item for top or bottom - one word answer"
    )

    messages = []
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": "llava",
        "messages": messages,
        "stream": False,
    }

    # Send POST request
    response = requests.post(url_llama, json=payload)

    # Check response
    if response.status_code == 200:
        result1 = response.json()["message"]["content"]
    else:
        return f"Request failed with status code: {response.status_code}"

    prompt = f"{path} give a one sentence description of this clothing item"

    messages = []
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": "llava",
        "messages": messages,
        "stream": False,
    }

    response = requests.post(url_llama, json=payload)

    if response.status_code == 200:
        result2 += response.json()["message"]["content"]
    else:
        return f"Request failed with status code: {response.status_code}"

    result = '["' + result1 + '","' + result2 + '"]'

    return result


# Connect to weather API
@app.route("/weather", methods=['post'])
def get_weather():
    zipcode = request.form.get("zipcode")
    api_key = "882d7c4617b36d2101b88c388111c3a0"
    url = f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&appid={api_key}&units=imperial"
    response = requests.get(url)
    weather_data = response.json()

    if response.status_code == 200:
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        description = weather_data["weather"][0]["description"]

        print(
            f"Temperature: {temperature} Farenheit\n Humidity: {humidity}%\n Description: {description}"
        )
        prompt = f"This is the weather in my city: Temperature: {temperature} Farenheit\n Humidity: {humidity}%\n Description: {description}"
        return prompt
    else:
        print("Error fetching weather data")


def generate_response(preferences):
    url_llama = "http://localhost:11434/api/chat"
    prompt = get_weather() + preferences
    db_return = insert.download_all(supabase, supabase.auth.get_user().user.id)

    messages = []
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": "mistral",
        "messages": messages,
        "stream": False,
    }

    # Send POST request
    response = requests.post(url_llama, json=payload)

    # Check response
    if response.status_code == 200:
        result = response.json()["message"]["content"]
        print(result)
        return result
    else:
        return f"Request failed with status code: {response.status_code}"


def name_similarity(a, b):
    # Returns score for string similarity from 0 to 1
    a = a.lower()
    b = b.lower()
    if a == b:
        return 1
    elif a in b or b in a:
        return (1 + SequenceMatcher(None, a, b).ratio()) / 2
    else:
        return (SequenceMatcher(None, a, b).ratio()) / 2


# Get preferences (outfit type)
def get_preferences():
    outfit_type = input("Enter 1 for Casual, 2 for Semi-formal, 3 for Formal")
    return outfit_type


# Get info for DB


def generate_outfit():
    # Get weather
    get_weather()
    # Get preferences
    preferences = get_preferences()

    generate_response(requests.Session(), preferences)

    return outfit


@app.route("/final")
def final():
    # set page to final.html

    return render_template("final.html")


@app.route("/image/<int:image_id>")
def display_image(image_id):
    # Get image data from the database
    image_data = get_image_from_database(image_id)

    # Return image data as response
    return send_file(image_data, mimetype="image/jpeg")


@app.route("/upload", methods=["POST"])
def upload():
    user = supabase.auth.get_user()
    print(user)
    # if not user:
    #     return redirect('/')
    uploaded_file = request.files["file"]
    uploaded_file.save("uploads/" + uploaded_file.filename)
    name = "uploads/" + uploaded_file.filename
    print(uploaded_file)
    try:
        id = insert.insert(
            supabase, user.user.id, name, "working file please please please"
        )
        print(id)
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(e)
    # os.remove(name)
    print(uploaded_file)
    return render_template("main.html")


@app.route("/evan")
def evan():
    user = supabase.auth.get_user()
    try:
        print("!!!!!!!!!!!!!!!!!!!!!")
        print(user.user.id)
    except Exception as e:
        print(e)
        print("error")
    return render_template("main.html")


@app.route("/insertMeth")
def insertMeth():
    try:
        user = supabase.auth.get_user()
        id = user.user.id
        id = insert.insert(supabase, id, "hello.png", "new file")
        print(id)
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!")
        print(e)
    return render_template("main.html")


@app.route("/login_evan")
def login_evan():

    try:
        data, error = supabase.auth.sign_in_with_password(
            {"email": "evanlmiller20@gmail.com", "password": "password1"}
        )
    except:
        return redirect("/")

    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug=True)
