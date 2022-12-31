import openai
import pyttsx3
import speech_recognition as sr
import sys
import threading

# Set up the ChatGPT API client
openai.api_key = "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"

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
sleeping = False

def speak(text):
  engine.say(text)
  engine.runAndWait()


def listen():
  with sr.Microphone() as source:
    if sleeping == False:
        print("Voice receiving……")
    else:
        print("Say Jarvis to wake me up")
    audio = r.listen(source)
  try:
    text = r.recognize_google(audio,language="en-EN")
    return text
  except Exception as e:
    str(e)
    return None

def generate_response(prompt):
  completions = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    n=1,
    max_tokens=2048,
    stop=None
  )
  message = completions.choices[0].text
  return message

speak("I'm Jarvis, the third generation AI. What can I do to help you?")


while True:
    prompt = listen()
    if prompt == "Shutdown":
        speak("See you next time.")
        sys.exit()

    elif sleeping == True:
        if prompt == "Jarvis":
            sleeping = False
            speak("I'm here.")
        else:
            print(prompt,"is what?")

    elif sleeping == False:
        if prompt == "Sleep":
            sleeping = True
            speak("Sleeping……")
        elif prompt is None:
            speak("What?")
        else:
            # Set up a timer to interrupt the text-to-speech engine after 10 seconds
            timer = threading.Timer(8.0, engine.stop)
            timer.start()

            # Speak the response
            print("You asked:",prompt)
            response = generate_response(prompt)
            speak(response+".Here are my notes.")
            print("Jarvis: ",response)

            # Cancel the timer if the response finishes speaking before it expires
            timer.cancel()
