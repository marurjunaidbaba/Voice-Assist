import speech_recognition as sr
import requests
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


try:
    with mic as source:
        print("Say the 'Code Word' to proceed: ")
        audio = recon.listen(source)
    
    command = recon.recognize_google(audio).lower()
    if command == "code word":
        print("Hello Boss.")
        print("Tell me the city for which you want the weather!")
        with mic as source:
            recon.adjust_for_ambient_noise(source)
            audio = recon.listen(source)
            text = recon.recognize_google(audio)
        city = recon.recognize_google(audio)
        print(f"You said: {city}")
        weather_info = get_weather(city)
        print(weather_info)
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError:
    print("Could not request results; Check your internet connection.")
except Exception as e:
    print(f"An error occurred: {e}")