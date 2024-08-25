import pyttsx3
import speech_recognition as sr
import time
import eel

def speak(text):
    text=str(text)
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    engine.setProperty('rate',174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        eel.DisplayMessage('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)        
        audio = r.listen(source, 10, 6)
    try:
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        return ""
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query=takeCommand()
        eel.senderText(query)
    else:
        query=message
        eel.senderText(query)
    try:
        if "phone call" in query or "video call" in query:
            from engine.features import findContact,whatsApp
            flag=""
            contact_no,name=findContact(query)
            if(contact_no != 0):
                if "phone call" in query:
                    flag='call'
                else:
                    flag='video call'
                whatsApp(contact_no,query,flag,name)
        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("Error")

    eel.ShowHood()