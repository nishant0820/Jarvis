from pipes import quote
import struct
import subprocess
import time
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.config import ASSISTANT_NAME
from engine.command import speak
import os
from hugchat import hugchat
import pvporcupine
import sqlite3

from engine.helper import remove_words

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir="www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)
            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)
            # checking first keyword detetcted for not
            if keyword_index>=0:
                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)
    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str
        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

def whatsApp(mobile_no, message, flag, name):
    if flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "Calling to "+name
    else:
        target_tab = 6
        message = ''
        jarvis_message = "Staring Video Call with "+name
    # Encode the message for URL
    encoded_message = quote(message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'
    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')

    speak(jarvis_message)

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    eel.DisplayMessage(response)
    print(response)
    speak(response)
    return response

# Android automation
def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)
