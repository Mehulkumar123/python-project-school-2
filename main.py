import speech_recognition as sr
import wikipediaapi
from gtts import gTTS
import os
import json
import requests
import time

try:
    with open("qa_data.txt", "r") as f:
        qa_dict = json.load(f)
except FileNotFoundError:
    qa_dict = {}
except json.JSONDecodeError:
    print("Error: Could not load Q&A data from file.")
    qa_dict = {}

r = sr.Recognizer()
wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

def save_data(qa_dict):
    try:
        with open("qa_data.txt", "w") as f:
            json.dump(qa_dict, f)
    except:
        print("Error: Could not save Q&A data to file.")

def play_audio(answer):
    try:
        tts = gTTS(answer)
        tts.save("answer.mp3")
        os.system("mpg321 answer.mp3")
    except:
        print("Error: Could not convert text to speech.")

while True:
    try:
        with sr.Microphone() as source:
            print("Ask a question or give a command:")
            audio = r.listen(source)
    except:
        print("Error: Could not listen to microphone input.")
        continue

    try:
        command = r.recognize_google(audio).lower()
        print("Command:", command)
    except sr.UnknownValueError:
        print("Error: Could not recognize speech.")
        continue
    except sr.RequestError as e:
        print(f"Error: {e}")
        continue

    if command == "stop":
        break
    elif command == "pause":
        os.system("pkill mpg321")
        continue
    elif command == "resume":
        try:
            with sr.Microphone() as source:
                print("Ask a question or give a command:")
                audio = r.listen(source)
        except:
            print("Error: Could not listen to microphone input.")
            continue

        try:
            question = r.recognize_google(audio).lower()
            print("Question:", question)
        except sr.UnknownValueError:
            print("Error: Could not recognize speech.")
            continue
        except sr.RequestError as e:
            print(f"Error: {e}")
            continue
    else:
        question = command

    answer = qa_dict.get(question)
    if answer:
        print("Answer:", answer)
    else:
        response = requests.get(f"https://api.duckduckgo.com/?q={question}&format=json")
        try:
            response_json = response.json()
        except:
            print("Error: Could not retrieve response from DuckDuckGo API.")
            continue

        if response_json.get("Abstract"):
            answer = response_json["AbstractText"]
            print("Answer:", answer)
            qa_dict[question] = answer
            save_data(qa_dict)
        else:
            page = wiki.page(question)
            if page.exists():
                answer = page.text[0:min(len(page.text), 500)] + "..."
                print("Answer:", answer)
                qa_dict[question] = answer
                save_data(qa_dict)
            else:
                print("Sorry, I don't know the answer.")
                continue

    try:
        tts = gTTS(answer)
        tts.save("answer.mp3")
        os.system("mpg321 answer.mp3")
    except:
        print("Error: Could not convert text to speech.")
        continue
