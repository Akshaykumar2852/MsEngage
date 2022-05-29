import speech_recognition as sr
from pynput.keyboard import Controller as key_controller
from pynput.keyboard import Key
import time
import os
import Assistant

voice = sr.Recognizer()
keyboard = key_controller()

def writter():
    while True:
        with sr.Microphone() as source:
            print ('listening for notepad.....')
            data = voice.listen(source)
            data_final = voice.recognize_google(data)

                Assistant.TaskExecution()

            print ('Typing.....')
            for x in data_final:
                 keyboard.type(x)
                 # time.sleep(0.1)
            keyboard.press(Key.enter)