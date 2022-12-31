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
        print("语音接收中……")
    else:
        print("说“小娜”来唤醒我。")
    audio = r.listen(source)
  try:
    text = r.recognize_google(audio,language="zh-ZH")
    if check == 1:
        print("你说：",text)
    if check == 0:
        print("那是什么？")
    return text
  except Exception as e:
    if check == 1:
        print("小娜: 什么？")
    elif check == 0:
        print("那是什么？")
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

speak("我是小娜,第三代人工智能，我能帮助你些什么？")
check = 1

while True:
  prompt = listen()
  if check == 0 and prompt =="小娜":
      check = 1
      speak("请说。")

  elif check == 1:
    if prompt == "开始睡眠":
      check = 0
      speak("休眠中……")
    elif prompt == "关机":
      # Exit the program
      speak("电脑关机。")
      sys.exit()
    elif prompt is None:
        speak("什么？")
    else:
        # Set up a timer to interrupt the text-to-speech engine after 10 seconds
        timer = threading.Timer(8.0, engine.stop)
        timer.start()

        # Speak the response
        response = generate_response(prompt)
        speak(response+"。以下是我准备的笔记。")
        print("小娜：",response)

        # Cancel the timer if the response finishes speaking before it expires
        timer.cancel()
