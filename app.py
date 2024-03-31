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
level = "casual"


@app.route("/")
def home():
    user = supabase.auth.get_user()

    if user:
        # print(user)
        return render_template("main.html")
    else:
        return render_template("login.html")


@app.route("/casual")
def casual():
    return render_template("preferences.html")


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
            return str(base64_data)
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def llava_scan(path):
    url_llama = "http://localhost:11434/api/generate"

    base64_image = image_to_base64(path)
    print("WOmp womp womp womp womp")
    prompt = "Classify this as a clothing item for top or bottom - one word answer"

    payload = {
        "model": "llava",
        "prompt": prompt,
        "stream": False,
        "images": [base64_image],
        "keep_alive": 1000,
    }

    # Send POST request
    response = requests.post(url_llama, json=payload)
    print("WOmp womp womp womp womp1")

    # Check response
    if response.status_code == 200 or response.status_code == 201:
        result1 = response.json()["response"]
        # print(response.json())
    else:
        return f"Request failed with status code: {response.status_code} 111111"

    prompt = "Give a one sentence description of this clothing item"

    payload = {
        "model": "llava",
        "prompt": prompt,
        "stream": False,
        "images": [base64_image],
    }

    response = requests.post(url_llama, json=payload)
    print("WOmp womp womp womp womp2")

    if response.status_code == 200 or response.status_code == 201:
        result2 = response.json()["response"]
        # print(response.json())
    else:
        return f"Request failed with status code: {response.status_code} 222222"

    result = result1 + ":" + result2
    return result

def get_weather(zip):
    if zip is None:
        zip = 47906
    zipcode = zip
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


def generate_response(inputs, zip):
    print(f"........{zip}")
    print(f"!!!!!!!!!!!!!!!!!!!!!!{inputs}")
    url_llama = "http://localhost:11434/api/generate"
    prompt = get_weather(zip) + inputs
    prompt += " Choose just 1 top and 1 bottom from the following options that go well together."
    db_return_raw = insert.download_all(supabase, supabase.auth.get_user().user.id)
    db_return = str(db_return_raw)
    print("downloaded")
    prompt += db_return

    prompt += "\nChoose one labeled as a top and one labeled as a bottom. Respond in the same format as the input list. Do not output any other information or any wrong information."
    print(prompt)
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
    }

    print("did it get here")
    # Send POST request
    response = requests.post(url_llama, json=payload)
    # Check response
    if response.status_code != 200:
        return f"Request failed with status code: {response.status_code}"

    result = response.json()["response"]
    # print(result)
    result_sim_list = []
    result_sim_names = []
    result_sim_list_bottom = []
    # result_sim_names_bottom = []
    # print(db_return_raw)
    for item in db_return_raw:
        a = item["description"]
        result_sim_names.append(item["id"])
        if "top" in a.lower():
            result_sim_list.append(name_similarity(str(a), str(result)))
            result_sim_list_bottom.append(0)
        elif "bottom" in a.lower():
            result_sim_list_bottom.append(name_similarity(str(a), str(result)))
            result_sim_list.append(0)
        else:
            result_sim_list_bottom.append(name_similarity(str(a), str(result)))
            result_sim_list.append(0)

    if len(result_sim_list) != 0 and len(result_sim_list_bottom) != 0:

        # print("Did the end get here ?!?!?!?")
        # print(result_sim_list)
        highest_index_top = result_sim_list.index(max(result_sim_list))
        highest_index_bottom = result_sim_list_bottom.index(max(result_sim_list_bottom))
        # print(highest_indices)
        display_ids = [
            result_sim_names[highest_index_top],
            result_sim_names[highest_index_bottom],
        ]
        print(highest_index_top, highest_index_bottom)
        # print(display_ids)
    else:
        raise Exception("Sufficient tops or bottoms NOT found")

    return display_ids


def name_similarity(a, b):
    # Returns score for string similarity from 0 to 1
    a = a.lower()
    b = b.lower()
    print("A" + a)
    print("B" + b)
    if a == b:
        return 1
    elif a in b or b in a:
        return (1 + SequenceMatcher(None, a, b).ratio()) / 2
    else:
        return (SequenceMatcher(None, a, b).ratio()) / 2


# # Get preferences (outfit type)
# def get_preferences():
#     outfit_type = input("Enter 1 for Casual, 2 for Semi-formal, 3 for Formal")
#     return outfit_type


# Get info for DB


# def generate_outfit():
#     # Get weather
#     get_weather()
#     # Get preferences
#     name = get_preferences()

#     generate_response(requests.Session(), name)

#     return outfit


@app.route("/final", methods=["post"])
def final():

    # set page to final.html
    print("Enter the function")
    a = request.form.get("message")
    zipcode = request.form.get("zipcode")
    if a is None:
        a = "casual"
    if zipcode is None:
        zipcode = 47906
    print(zipcode)
    print(a)
    print("ENter the function")
    try:
        output = generate_response(". Preference is " + a, zipcode)
    except:
        output = generate_response(". Preference is " + a, 47906)
    print("Response generated")
    id = supabase.auth.get_user().user.id
    image_path1 = id + "_" + str(output[0]) + ".jpg"
    image_path2 = id + "_" + str(output[1]) + ".jpg"
    try:
        insert.download(supabase, image_path1, "uploads/top.jpg")
    except Exception as e:
        print("error1")
        print(e)
    try:
        insert.download(supabase, image_path2, "uploads/bottom.jpg")
    except Exception as e:
        print("error2")
        print(e)

    if supabase.auth.get_user():
        return render_template("final.html")
    else:
        return render_template("login.html")


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
    # if not user:
    #     return redirect('/')
    uploaded_file = request.files["file"]
    uploaded_file.save("uploads/" + uploaded_file.filename)
    name = "uploads/" + uploaded_file.filename
    description = llava_scan(name)
    try:
        print("Did this work")
        id = insert.insert(supabase, user.user.id, name, description)
        print(id)
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!`1`1")
        print(e)
    # os.remove(name)
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
