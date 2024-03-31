import insert
import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
url = "https://rzdyvqcuzbdcaibdrypw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ6ZHl2cWN1emJkY2FpYmRyeXB3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE4MTQ1MzksImV4cCI6MjAyNzM5MDUzOX0.pqHVSybnPnXseAdDJ3bhTWUsmq7n3j-iGFRt_R4RnQQ"
supabase: Client = create_client(url, key)

id = insert.insert(supabase, "evan", "image.jpg", "green cloak")
id = insert.insert(supabase, "evan", "Images/acne2.png", "white shirt")
id = insert.insert(supabase, "evan", "Images/clothingimage1.png", "blue sweater")
data = insert.download_all(supabase, "evan")
for item in data:
    print(item)
