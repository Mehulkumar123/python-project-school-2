import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# A list of Q&A pairs
questions_answers = {
    "what's your name": "My name is wasd.",
    "how old are you": "I was trained by ClosedBD(biological Dummy), so I don't have an age.(He did not bother to give me  an age yo yeah)",
    "what do you do": "I am a language model that can answer questions and generate text.(That's lie use google dummy)",
}

# Function to listen to the speech and return text
def listen_to_speech():
    # Reading Microphone as source
    with sr.Microphone() as source:
        print("Talk")
        audio = r.listen(source)
        print("Stop.")

    try:
        # using google to recognize speech
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except:
        print("Sorry, I did not get that.")
        return None

# Main loop
while True:
    text = listen_to_speech()
    if text:
        if text in questions_answers:
            print(questions_answers[text])
        else:
            print("I am not sure what you mean.")
