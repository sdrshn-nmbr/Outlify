import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
url= "https://rzdyvqcuzbdcaibdrypw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ6ZHl2cWN1emJkY2FpYmRyeXB3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE4MTQ1MzksImV4cCI6MjAyNzM5MDUzOX0.pqHVSybnPnXseAdDJ3bhTWUsmq7n3j-iGFRt_R4RnQQ"
supabase: Client = create_client(url, key)

def insert(user_id, image_path):
    path_on_supastorage = "a.jpg"
    data, count = supabase.table(user_id).insert({"description": "new"}).execute()
    id = data[1][0]['id']
    path_on_supastorage = user_id + "_" + str(id) + ".jpg"
    with open(image_path, 'rb') as f:
        supabase.storage.from_("Clothes").upload(file=f,path=path_on_supastorage, file_options={"content-type": "jpg"})
    return id

def download(image_path, destination):
    with open(destination, 'wb+') as f:
        res = supabase.storage.from_("Clothes").download(image_path)
        f.write(res)