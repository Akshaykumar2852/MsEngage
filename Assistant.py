import pyautogui
import pyttsx3
import speech_recognition as sr
import datetime
import os
import pywhatkit
import wikipedia
import pyjokes
import webbrowser
from requests import get
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 160)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    speak("All systems online...")
    if hour >= 0 and hour < 12:
        speak("Good Morning sir. How may I help you?")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon sir. How may I help you?")

    else:
        speak("Good Evening sir. How may I help you?")

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=8, timeout=3)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        if "friday" in query:
            query="Wake up Friday"
        print(f"User said: {query}\n")
    except:
        return "none"
    return query


def TaskExecution():
    while True:
        query = takeCommand().lower()

        if "open notepad" in query:
            speak("Opening Notepad...")
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)

        elif "exit notepad" in query or "close notepad" in query:
            speak("Closing Notepad...")
            os.system("taskkill /f /im notepad.exe")

        elif "open command prompt" in query or "cmd" in query:
            os.system("start cmd")

        elif "play some music" in query or "play music" in query:
            speak("What song would you like to play")
            song = takeCommand()
            if song == "none":
                song="a random song"
            song = song.replace("play", "")
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'time' in query or "what time" in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Current time is {strTime}")

        elif ('search for' or 'wikipedia' or 'get info on' or 'tell me about') in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "") or query.replace("search for", "") or query.replace(
                "get info on", "") or query.replace("tell me about", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia : ")
            speak(results)

        elif "joke" in query or "tell me a joke" in query:
            speak("Here's a joke : ")
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'open youtube' in query or "youtube" in query:
            speak("Opening Youtube...")
            webbrowser.open("youtube.com")

        elif 'open google' in query or "google" in query:
            speak("Opening Google...")
            webbrowser.open("google.com")

        elif 'open stack overflow' in query or "stack overflow" in query:
            speak("Opening Stackoverflow...")
            webbrowser.open("stackoverflow.com")

        elif "ip address" in query:
            ip = get("https://api.ipify.org").text
            speak(f"Your IP address is : {ip}")

        elif "go to sleep" in query or 'shut down' in query or 'shutdown' in query or 'sleep' in query:
            speak("All systems shutting down...")
            sys.exit()

        elif "switch tabs" in query or "switch tab" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")

        elif "none" in query:
            TaskExecution()

        else:
            pass