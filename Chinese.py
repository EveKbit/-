import openai
import pyttsx3
import speech_recognition as sr
import sys
import threading

# Set up the ChatGPT API client
openai.api_key = "Your-API-Key"

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
        print("语音接收中……")
    else:
        print("说“小唐”来唤醒我。")
    audio = r.listen(source)
  try:
    text = r.recognize_google(audio,language="zh-ZH")
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

speak("我是小唐,第三代人工智能，我能帮助你些什么？")


while True:
    prompt = listen()
    if prompt == "关机":
        speak("下次再见。")
        sys.exit()

    elif sleeping == True:
        if prompt == "小唐":
            sleeping = False
            speak("我在。")
        else:
            print(prompt,"是什么？")

    elif sleeping == False:
        if prompt == "睡眠":
            sleeping = True
            speak("休眠中……")
        elif prompt is None:
            speak("什么?")
        else:
            # Set up a timer to interrupt the text-to-speech engine after 10 seconds
            timer = threading.Timer(8.0, engine.stop)
            timer.start()

            # Speak the response
            print("你说:",prompt)
            response = generate_response(prompt)
            speak(response+"。以下是我整理的笔记。")
            print("小唐: ",response)

            # Cancel the timer if the response finishes speaking before it expires
            timer.cancel()
