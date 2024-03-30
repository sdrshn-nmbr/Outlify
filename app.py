from flask import Flask, request, redirect, url_for
#from postgrest_py import PostgrestClient
from dotenv import load_dotenv
import os

from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client('https://yhjgqrrmkmbkiunfwxbo.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InloamdxcnJta21ia2l1bmZ3eGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE4MTQzODIsImV4cCI6MjAyNzM5MDM4Mn0.BLD1z5AuIYV77SKF8t0z5gJIHJ88MyFAkBvo4Kc3PO0')

load_dotenv()
app = Flask(__name__)

@app.route("/")
def test():

    choice = 0

    while choice != '-1':

        choice = input("Sign Up, Sign In, Sign Out, View Data (1, 2, 3, 4): ")

        if choice == "1":
            email = input("Email: ")
            password = input("Password: ")
            res = supabase.auth.sign_up(
                {
                    'email': email,
                    'password': password
                }
            )
            #print(res)
        elif choice == '2':
            email = input("Email: ")
            password = input("Password: ")
            data, error = supabase.auth.sign_in_with_password({"email": email, "password": password})
            print(data)
            #if error:
            #    print(error)
            #    return {'error': error.message}, 400
        elif choice == '3':
            res = supabase.auth.sign_out()
        elif choice == '4':
            data = supabase.auth.get_user()
            print(data.user.id)
    
    
    return "Hello"


def forward_string():
    llm_prompt = input("Prompt: ")
    return llm_prompt

# Connect to weather API

# Call ollama

# Get preferences (outfit type)
def get_preferences():
    outfit_type = input("Enter 1 for Casual, 2 for Semi-formal, 3 for Formal")
    return outfit_type

# Get info for DB


if __name__ == "__main__":
    app.run(debug=True)