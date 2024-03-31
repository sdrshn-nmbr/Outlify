# Outlify

Outlify is an application that helps you look good with your own clothes! It uses open source AI to suggest outfits based on your personal wardrobe.

## Project Structure

The project is structured as follows:

- `app.py`: The main application file.
- `insert.py`: Supabase DB logic
- `hacker/`: virtual environment for all packages required -> activate using `source hacker/bin/activate`
- `Images/`: Contains images used in the application.
- `static/`: Contains static files like CSS and JavaScript for the web application.
- `templates/`: Contains HTML templates for the web application.

## Setup

1. Clone the repository.
2. Download Ollama from https://ollama.com/
3. Install the required Python packages using pip:

```sh
pip install -r requirements.txt