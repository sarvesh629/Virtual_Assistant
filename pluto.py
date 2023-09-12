import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import subprocess
import os
import spotipy
import smtplib
import requests
import json


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("good morning Sir")
    elif hour>=12 and hour<17:
        speak("Good afternoon Sir")
    else:
        speak("Good Evening Sir")
        
    speak("My name is Pluto. How may I assist you?")

def takeCommand():
    # Microphone input and string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    
    except Exception as e:
        #print(e)
        print("Say that again please...")
        return "None"
    return query 

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    #Enter the email id details you want to login frmo
    server.sendmail('youremail@gmail.com', to, content)
    server.close()
    

def get_recipe(query):
    base_url = "http://www.recipepuppy.com/api/"
    params = {
        "q": query,
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if "results" in data and len(data["results"]) > 0:
        recipe = data["results"][0]
        title = recipe["title"]
        ingredients = recipe["ingredients"]
        
        recipe_info = f"Here's a recipe for {title}. Ingredients include: {ingredients}."
        return recipe_info
    else:
        return "Sorry, I couldn't find a recipe for the item you requested."    

if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()
        
        if 'wikipedia' in query:
            speak("Searching in Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query,sentences=2)
            speak("According to wikipedia, ")
            print(results)
            speak(results)
        
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open your master' in query:
            webbrowser.open("chat.openai.com")
            
        elif 'play music' in query:
            #subprocess.Popen(['spotify'])
            webbrowser.open("https://open.spotify.com/track/1TfqLAPs4K3s2rJMoCokcS?si=9d24699b08e74775")
            # speak("Sure, what song would you like to play?")
            # song_name = takeCommand().lower()

            # # Search for the song in Spotify
            # results = sp.search(q=song_name, limit=1, type='track')

            # if len(results['tracks']['items']) > 0:
            #     track_uri = results['tracks']['items'][0]['uri']
            #     sp.start_playback(uris=[track_uri])
            #     speak(f"Now playing {results['tracks']['items'][0]['name']} by {results['tracks']['items'][0]['artists'][0]['name']}")
            # else:
            #     speak("Sorry, I couldn't find that song.")
                
                
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        
        elif 'open code' in query:
            codePath = "C:\\Users\\Sarvesh\\AppData\\Local\\Programs\\Microsoft VS Code\Code.exe"
            os.startfile(codePath)
            
        elif 'email to sarvesh' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "sarveshsankaran@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email")
        
        elif 'recipe' in query:
            speak("Sure, please tell me what recipe you'd like to search for.")
            recipe_query = takeCommand().lower()
            recipe_info = get_recipe(recipe_query)
            print(recipe_info)
            speak(recipe_info)