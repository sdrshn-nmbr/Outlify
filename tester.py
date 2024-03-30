import insert

id = insert.insert("evan", "image.jpg", "green cloak")
id = insert.insert("evan", "Images/acne2.png", "white shirt")
id = insert.insert("evan", "Images/clothingimage1.png", "blue sweater")
data = insert.download_all("evan")
for item in data:
    print(item)
