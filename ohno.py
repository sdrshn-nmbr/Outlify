


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

