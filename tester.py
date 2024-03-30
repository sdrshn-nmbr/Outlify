import insert

id = insert.insert("evan", "image.jpg", "green cloak")
id = insert.insert("evan", "receipt.jpg", "not clothes")
id = insert.insert("evan", "vscode.png", "screenshot of code")
data = insert.download_all("evan")
for item in data:
    print(item)
