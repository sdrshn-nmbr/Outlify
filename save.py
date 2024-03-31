@app.route("/preferences")
def preferences():
    user = supabase.auth.get_user()

    if user:
        # print(user)
        return render_template("preferences.html")
    else:
        return render_template("login.html")
    

@app.route("/uploads/top")
def display_top():
    # Get image data from the database
    print("Yahoo")
    # image_data = get_image_from_database(image_id)
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