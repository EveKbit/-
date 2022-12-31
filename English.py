from cmath import e
from distutils.command.check import check
import openai
import pyttsx3
import speech_recognition as sr
import sys
import threading

# Set up the ChatGPT API client
openai.api_key = "Your_API"

# Set up the text-to-speech engine
engine = pyttsx3.init()

#get the available voices
voice = engine.getProperty('voices')

# Set the voice to use
engine.setProperty('voice', voice[0].id)


# Set the volume
engine.setProperty('volume', 1.0)

# Set the rate at which the words are spoken
engine.setProperty('rate', 180)

# Set up the speech recognition engine
r = sr.Recognizer()


def speak(text):
  engine.say(text)
  engine.runAndWait()


def listen():
  with sr.Microphone() as source:
    if check == 1:
        print("Voice receiving")
    else:
        print("Say "Jarvis" to wake me up")
    audio = r.listen(source)
  try:
    text = r.recognize_google(audio,language="en-EN")
    if check == 1:
        print("You asked：",text)
    if check == 0:
        print("What's that?")
    return text
  except Exception as e:
    if check == 1:
        print("Jarvis: What?")
    elif check == 0:
        print("What's that?")
    return None


def generate_response(prompt):
  if check == 1:
    completions = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      n=1,
      stop=None
  )
    message = completions.choices[0].text
    return message
  if check == 0:
      return None

speak("I'm Jarvis, the third generation AI. What can I do to help you?")
check = 1

while True:
  prompt = listen()
  if check == 0 and prompt =="Jarvis":
      check = 1
      speak("Please")

  elif check == 1:
    if prompt == "Sleep":
      check = 0
      speak("Sleeping")
    elif prompt == "Shutdown":
      # Exit the program
      speak("Computer shutdown")
      sys.exit()
    elif prompt is None:
        speak("What？")
    else:
        # Set up a timer to interrupt the text-to-speech engine after 10 seconds
        timer = threading.Timer(10.0, engine.stop)
        timer.start()

        # Speak the response
        response = generate_response(prompt)
        speak(response+".Here are my notes.")
        print("Jarvis：",response)

        # Cancel the timer if the response finishes speaking before it expires
        timer.cancel()
