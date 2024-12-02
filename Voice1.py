import speech_recognition as sr
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyaudio as pa

recon = sr.Recognizer()
mic = sr.Microphone()

def get_weather(city):
    api_key = "860b2ae4a2bbb8bc98bcaf51387135b6"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['cod'] == 200:
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temp = main['temp']
        return f"Current temperature in {city} is {temp} degree Celsius with {weather_desc}."
    else:
        return "City not found."

def get_artist_info(ar_name):
    client_id = "5632466abe9043dbac18d5aaa1edc448"
    client_secret = "3881b158f54745589b8cd5060ce7b147"

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.search(q='artist:' + ar_name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        artist_info = f"Name: {artist['name']}\nFollowers: {artist['followers']['total']}\nGenres: {', '.join(artist['genres'])}\nPopularity: {artist['popularity']}\n"
        return artist_info
    else:
        return "Artist not found."

print("Say 'Hey Jarvis' to wake me up:")

try:
    with mic as source:
        recon.adjust_for_ambient_noise(source)
        audio = recon.listen(source)

    wake_up_command = recon.recognize_google(audio).lower()
    if "hey jarvis" in wake_up_command:
        print("Hello Boss")

        with mic as source:
            recon.adjust_for_ambient_noise(source)
            print("Say 'weather in [city]' for weather information or 'info about [artist]' for artist information.")
            audio = recon.listen(source)

        query = recon.recognize_google(audio)
        print(f"You said: {query}")

        if query.lower().startswith("weather in"):
    #city = query.split("weather")[1].strip()
            city = query.replace("weather in", "").strip()
            weather_info = get_weather(city)
            print(weather_info)
        elif query.lower().startswith("info about"):
            artist_name = query.replace("info about", "").strip()
            artist_info = get_artist_info(artist_name)
            print(artist_info)
        else:
            print("Sorry boss, I couldn't understand the request.")


except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError:
    print("Could not request results; Check your internet connection.")
except Exception as e:
    print(f"An error occurred: {e}")