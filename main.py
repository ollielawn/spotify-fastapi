from fastapi import FastAPI
from dotenv import load_dotenv
import requests
import time
import json
import os

#load environment variables
load_dotenv()

#instantiate FastAPI
app = FastAPI()

#create token variable
access_token = None
#create log of token validity
token_expiry = 0

def access_token_validation():
    global access_token
    if access_token and time.time() < token_expiry:
        return access_token
    else:
        raise Exception("Access token invalid, run '/get_spotify_token' for new token")

#resassign environment variables
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"

@app.get("/")
def initial_connection():
    return {'message': "Hello world"}

@app.post('/get_spotify_token')
async def get_spotify_token():
    global access_token, token_expiry
    url = token_url
    headers = {'Content_Type': 'application/x-www-form-urlencode'}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url=url, headers=headers, data=data)
    json_response = response.json()
    print(json_response)
    access_token = json_response['access_token']
    token_expiry = time.time() + json_response["expires_in"]
    return json_response

@app.get('/find_artist/{artist_id}')
async def get_artist_info(artist_id):
    print(access_token_validation())
    if access_token_validation():
        url = f'https://api.spotify.com/v1/artists/{artist_id}'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url=url, headers=headers)
        response_data = response.json()
        return response_data



