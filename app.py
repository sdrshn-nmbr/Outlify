from flask import Flask, request, redirect, url_for, render_template
from difflib import SequenceMatcher
import base64
from PIL import Image

# from postgrest_py import PostgrestClient
from dotenv import load_dotenv
import os
import requests
from pprint import pprint as pp
import insert
import heapq

from supabase import create_client, Client

url = "https://rzdyvqcuzbdcaibdrypw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ6ZHl2cWN1emJkY2FpYmRyeXB3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE4MTQ1MzksImV4cCI6MjAyNzM5MDUzOX0.pqHVSybnPnXseAdDJ3bhTWUsmq7n3j-iGFRt_R4RnQQ"
supabase: Client = create_client(url, key)

app = Flask(__name__)


@app.route("/")
def home():
    user = supabase.auth.get_user()

    if user:
        # print(user)
        return render_template("main.html")
    else:
        return render_template("login.html")

@app.route("/preferences")
def preferences():
    user = supabase.auth.get_user()

    if user:
        # print(user)
        return render_template("preferences.html")
    else:
        return render_template("login.html")
    

@app.route("/signup")
def signup_page():
    return render_template("signup.html")


@app.route("/login_func", methods=["post"])
def login_func():
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        data, error = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!")
        print(e)
        return redirect("/")

    return redirect("/")


@app.route("/signup_func", methods=["post"])
def signup_func():
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
    except:
        return redirect("/signup")
    try:
        user = supabase.auth.get_user()
        id = user.user.id
        id = insert.create_user(supabase, id)
        print(id)
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!")
        print(e)

    return redirect("/")


@app.route("/signout")
def signout_func():
    res = supabase.auth.sign_out()
    return redirect("/")


def image_to_base64(image_path):
    try:
        # Open the image file
        with open(image_path, "rb") as img_file:
            # Read the image data
            img_data = img_file.read()
            # Encode the image data to base64
            base64_data = base64.b64encode(img_data).decode("utf-8")
            return base64_data
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def llava_scan(path):
    url_llama = "http://localhost:11434/api/chat"

    base64_image = image_to_base64(path)

    prompt = (
        f"{path} classify this as a clothing item for top or bottom - one word answer"
    )

    messages = []
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": "tinyllava",
        "messages": messages,
        "stream": False,
        "images": [f"{base64_image}"],
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
        "images": [f"{base64_image}"],
    }

    response = requests.post(url_llama, json=payload)

    if response.status_code == 200:
        result2 = response.json()["message"]["content"]
    else:
        return f"Request failed with status code: {response.status_code}"

    result = result1 + ":" + result2
    print(result)
    return result


# Connect to weather API
@app.route("/weather")
def get_weather():
    zipcode = input("Enter Zipcode: ")
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

    """
    db_return =
    [
        {id: '1', name: 'Top:Black crewneck t-shirt'},
        {id: '2', name: 'Top:White V-neck t-shirt'},
        {
        ...
    ]
    """


def generate_response(preferences):
    url_llama = "http://localhost:11434/api/chat"
    prompt = get_weather() + preferences
    prompt += " Choose just 1 top and 1 bottom from the following options that go well together."
    db_return_raw = insert.download_all(supabase, supabase.auth.get_user().user.id)
    db_return = str(db_return_raw)

    prompt += db_return

    prompt += "\nChoose one labeled as a top and one labeled as a bottom. Respond in the same format as the input list. Do not output any other information or any wrong information."

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
    if response.status_code != 200:
        return f"Request failed with status code: {response.status_code}"

    result = response.json()["message"]["content"]

    result_sim_list = []
    result_sim_names = []

    for item in db_return_raw:
        a = item["name"]
        result_sim_list.append(name_similarity(result_sim_list, result))
        result_sim_names.append(item["id"])

    highest_indices = heapq.nlargest(2, range(len(a)), key=lambda i: a[i])
    display_ids = [result_sim_names[i] for i in highest_indices]

    return display_ids


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


@app.route("/uploads/top")
def display_top():
    # Get image data from the database
    with open("uploads/top.jpg", "rb") as f:
        image_data = f.read()
    # Return image data as response
    return image_data

@app.route("/uploads/bottom")
def display_bottom():
    # Get image data from the database
    with open("uploads/bottom.jpg", "rb") as f:
        image_data = f.read()
    return image_data

@app.route("/upload", methods=["POST"])
def upload():
    user = supabase.auth.get_user()
    print(user)
    # if not user:
    #     return redirect('/')
    uploaded_file = request.files["file"]
    uploaded_file.save("uploads/" + uploaded_file.filename)
    name = "uploads/" + uploaded_file.filename
    print(name)
    description = llava_scan(name)
    try:
        id = insert.insert(supabase, user.user.id, name, description)
        print(id)
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(e.message)
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
