import requests
from pprint import pprint as pp


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


def generate_response(preferences):
    url_llama = "http://localhost:11434/api/chat"
    prompt = get_weather() + preferences
    prompt += """Choose just 1 top and 1 bottom from the following options that go well together.
    [
        (1, "Black crewneck t-shirt", "Top"),
        (2, "White V-neck t-shirt", "Top"),
        (3, "Navy blue polo shirt", "Top"),
        (4, "Red graphic t-shirt", "Top"),
        (5, "Black denim shorts", "Bottom"),
        (6, "White chino shorts", "Bottom"),
        (7, "Royal blue athletic shorts", "Bottom"),
        (8, "Red plaid shorts", "Bottom"),
        (9, "Black slim-fit jeans", "Bottom"),
        (10, "White linen pants", "Bottom"),
        (11, "Indigo blue jogger pants", "Bottom"),
        (12, "Crimson red cargo pants", "Bottom"),
        (13, "Black fedora hat", "Top"),
        (14, "White baseball cap", "Top"),
        (15, "Gray pullover hoodie", "Top"),
        (16, "Yellow zip-up hoodie", "Top"),
        (17, "Olive green button-up shirt", "Top"),
        (18, "Pink oxford shirt", "Top"),
        (19, "Teal half-zip sweatshirt", "Top"),
        (20, "Burgundy sweater vest", "Top"),
        (21, "Charcoal blazer", "Top"),
        (22, "Cream cardigan", "Top"),
        (23, "Denim jacket", "Top"),
        (24, "Tan trench coat", "Top"),
        (25, "Black pinstripe suit jacket", "Top"),
        (26, "White linen blazer", "Top"),
        (27, "Navy blue windbreaker", "Top"),
        (28, "Red bomber jacket", "Top"),
        (29, "Black leather motorcycle jacket", "Top"),
        (30, "White denim jacket", "Top"),
        (31, "Gray tweed vest", "Top"),
        (32, "Mustard yellow raincoat", "Top"),
        (33, "Olive green field jacket", "Top"),
        (34, "Coral blouson jacket", "Top"),
        (35, "Plum corduroy blazer", "Top"),
        (36, "Beige suede jacket", "Top"),
        (37, "Black hoodie vest", "Top"),
        (38, "White sleeveless hoodie", "Top"),
        (39, "Navy blue varsity jacket", "Top"),
        (40, "Red fleece pullover", "Top"),
        (41, "Black down vest", "Top"),
        (42, "White zip-up cardigan", "Top"),
        (43, "Gray knitted poncho", "Top"),
        (44, "Tan safari jacket", "Top"),
        (45, "Black wool pea coat", "Top"),
        (46, "White ski jacket", "Top"),
        (47, "Navy blue puffer jacket", "Top"),
        (48, "Blue striped button-up shirt", "Top"),
        (49, "Green floral print blouse", "Top"),
        (50, "Red plaid flannel shirt", "Top"),
        (51, "Black and white checkered shirt", "Top"),
        (52, "Purple paisley print scarf", "Top"),
        (53, "Orange geometric patterned skirt", "Bottom"),
        (54, "Yellow polka dot sundress", "Bottom"),
        (55, "Blue floral print maxi skirt", "Bottom"),
        (56, "Pink striped leggings", "Bottom"),
        (57, "Green camouflage cargo pants", "Bottom"),
        (58, "Red tartan plaid trousers", "Bottom"),
        (59, "Black and white houndstooth pants", "Bottom"),
        (60, "Gray argyle patterned socks", "Bottom"),
    ]
    Choose one labeled as a top and one labeled as a bottom. Respond in the same format as the input list. Do not output any other information or any wrong information.
    """

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


from difflib import SequenceMatcher
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


generate_response(" ")
