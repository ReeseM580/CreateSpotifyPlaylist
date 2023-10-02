from dotenv import load_dotenv
import os
import base64
import json
import requests
from requests import post, get
from urllib.parse import quote  # Add this import


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    # Properly URL-encode the query parameter
    encoded_artist_name = quote(artist_name)
    query = f"?q={encoded_artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_related_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["artists"]
    return json_result

def create_playlist(token, songs):
    user_id = get_user_id(token)
    #user_id = "7ayvx1k15fudeqtqj0pnlvhj0"
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)
    name = input("Enter playlist name: ")
    public = False
    playlist_data = {"name": name, "description": "", "public": public}
    json_result = json.dumps(playlist_data)
    response = requests.post(url, headers = headers, data = json_result)
    if response.status_code == 201:
        print("Playlist created successfully.")
    else:
        print("Error creating the playlist. Status code:", response.status_code)
        print(response.json())

"""def get_user_id():
    url = f"https://api.spotify.com/v1/me"
    headers = get_auth_header(token)#need to pass user id or user token 
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data["id"]
        print("got user id", user_id)
        return user_id
    else:
        print("Error fetching user profile:", response.status_code)"""
    
"""Authorization url
https://accounts.spotify.com/authorize
Token url
https://accounts.spotify.com/api/token
"""


token = get_token()

artist = input("Enter an artist name: ")
result = search_for_artist(token, artist)
artist_id = result["id"]
"""relatedArtists = get_related_artists(token, artist_id)
for idx, song in enumerate(relatedArtists):
    print(f"{idx + 1}. {song['name']}")"""

songs = get_songs_by_artist(token, artist_id) 
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")

create_playlist(token, songs)
    
