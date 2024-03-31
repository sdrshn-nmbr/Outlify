# Outlify

Outlify is an application designed to enhance your style by suggesting outfits from your personal wardrobe, powered by open-source multi-modal LLM technology.

## Project Structure

The project is organized as follows:

- `app.py`: The primary application file.
- `insert.py`: Logic for Supabase database operations.
- `hacker/`: Virtual environment containing all required packages. Activate using `source hacker/bin/activate`.
- `Images/`: Directory holding images utilized within the application.
- `static/`: Stores static files such as CSS and JavaScript for the web application.
- `templates/`: Holds HTML templates for the web application.

## Setup

To set up the project:

1. Clone the repository.
2. Download Ollama from [Ollama.com](https://ollama.com/).
3. Install the necessary Python packages using pip:

```sh
pip install -r requirements.txt
```

## Demos

### Login

<img src="static/demo_imgs/login.jpeg" alt="Login Page" width="200">


## Home

<img src="static/demo_imgs/main.jpeg" alt="Home Page" width="200">


## Preferences

<img src="static/demo_imgs/preferences.jpeg" alt="Preferences Page" width="200">


## Outfit

<img src="static/demo_imgs/outfit.jpeg" alt="Outfit Page" width="200">


## Re-outlify

<img src="static/demo_imgs/reoutlify.jpeg" alt="Re-outlify Page" width="200">