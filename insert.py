
def insert(supabase, user_id="evan", image_path="hello.png", description="default response"):
    data, count = supabase.table(user_id).insert({"description": description}).execute()
    id = data[1][0]['id']
    path_on_supastorage = user_id + "_" + str(id) + ".jpg"
    supabase.storage.from_("Clothes").upload(file=image_path,path=path_on_supastorage, file_options={"content-type": "jpg"})
    return id

def download(supabase, image_path, destination):
    with open(destination, 'wb+') as f:
        res = supabase.storage.from_("Clothes").download(image_path)
        f.write(res)

def download_all(supabase, user_id):
    response = supabase.table(user_id).select("id", "description").execute()
    return response.data

def create_user(supabase, user_id):
    data, count = supabase.table(user_id).insert({"description": ""}).execute()
    return data
