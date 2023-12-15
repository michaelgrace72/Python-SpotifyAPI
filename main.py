from dotenv import load_dotenv
import os
import base64
import requests
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    url = "https://accounts.spotify.com/api/token"

    payload = {'grant_type': 'client_credentials'}
    # encode client_id and client_secret in base 64
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        'Authorization': 'Basic ' + auth_header,
        'content-type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)['access_token']




def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}

def search_artist(token, artist_name):
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"

    headers = get_auth_header(token)

    response = requests.request("GET", url, headers=headers)

    result =  json.loads(response.text)['artists']['items'][0]
    
    if len(result) == 0:
        print("No artist found")
        return None
    
    return result

def songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"

    headers = get_auth_header(token)

    response = requests.request("GET", url, headers=headers)

    result = json.loads(response.text)['tracks']
    
    if len(result) == 0:
        print("No songs found")
        return None
    
    return result

token = get_token()
artist = search_artist(token, "Michael Buble")
artist_id = artist["id"]
songs = songs_by_artist(token, artist_id)

for i, song in enumerate(songs):
    print(f"{i+1}. {song['name']}")
