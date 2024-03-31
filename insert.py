def insert(
    supabase, user_id="evan", image_path="hello.png", description="default response"
):
    try:
        data = (
            supabase.table("Users")
            .insert({"description": description, "user_id": user_id})
            .execute()
        )
    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(e)

    id = data.data[0]["id"]
    path_on_supastorage = user_id + "_" + str(id) + ".jpg"
    supabase.storage.from_("Clothes").upload(
        file=image_path, path=path_on_supastorage, file_options={"content-type": "jpg"}
    )
    return id


def download(supabase, image_path, destination):
    with open(destination, "wb+") as f:
        res = supabase.storage.from_("Clothes").download(image_path)
        f.write(res)


def download_all(supabase, user_id):
    response = (
        supabase.table("Users")
        .select("id", "description", "user_id")
        .eq("user_id", user_id)
        .execute()
    )
    return response.data
